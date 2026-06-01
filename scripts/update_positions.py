import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
import websockets

AISSTREAM_URL = "wss://stream.aisstream.io/v0/stream"
LISTEN_SECONDS = 300


def load_mmsi_list(rigs_path):
    with open(rigs_path) as f:
        rigs = yaml.safe_load(f)
    if not rigs:
        return []
    return [int(r["mmsi"]) for r in rigs if r.get("mmsi")]


async def fetch_positions(api_key, mmsi_list, positions):
    subscription = {
        "APIKey": api_key,
        "BoundingBoxes": [[-90, -180], [90, 180]],
        "FiltersShipMMSI": mmsi_list,
    }
    try:
        async with websockets.connect(AISSTREAM_URL) as ws:
            await ws.send(json.dumps(subscription))
            await asyncio.sleep(1)
            print("Subscription sent.")
            print(f"Connected. Listening for {LISTEN_SECONDS}s...")
            deadline = time.monotonic() + LISTEN_SECONDS
            while time.monotonic() < deadline:
                remaining = deadline - time.monotonic()
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=min(10.0, remaining))
                except asyncio.TimeoutError:
                    continue
                try:
                    msg = json.loads(raw)
                    if msg.get("MessageType") != "PositionReport":
                        continue
                    meta = msg.get("MetaData", {})
                    report = msg.get("Message", {}).get("PositionReport", {})
                    mmsi = str(meta.get("MMSI", ""))
                    lat = report.get("Latitude")
                    lng = report.get("Longitude")
                    ts = meta.get("time_utc") or datetime.now(timezone.utc).isoformat()
                    if mmsi and lat is not None and lng is not None:
                        positions[mmsi] = {"lat": lat, "lng": lng, "timestamp": ts}
                        print(f"  {mmsi}: {lat:.4f}, {lng:.4f}")
                except Exception as e:
                    print(f"  Warning: skipping malformed message: {e}", file=sys.stderr)
    except Exception as e:
        import traceback
        print(f"WebSocket error ({type(e).__name__}): {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("Writing whatever was captured...", file=sys.stderr)


def main():
    api_key = os.environ.get("AISSTREAM_API_KEY")
    if not api_key:
        print("Error: AISSTREAM_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    rigs_path = Path("_data/rigs.yml")
    if not rigs_path.exists():
        print(f"Error: {rigs_path} not found.", file=sys.stderr)
        sys.exit(1)

    mmsi_list = load_mmsi_list(rigs_path)
    if not mmsi_list:
        print("No rigs with MMSI in _data/rigs.yml. Exiting.", file=sys.stderr)
        sys.exit(0)

    print(f"Tracking {len(mmsi_list)} MMSIs: {', '.join(str(m) for m in mmsi_list)}")

    positions = {}
    asyncio.run(fetch_positions(api_key, mmsi_list, positions))

    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "positions.json"
    with open(out_path, "w") as f:
        json.dump(
            {"last_updated": datetime.now(timezone.utc).isoformat(), "positions": positions},
            f, indent=2,
        )

    print(f"\nCaptured {len(positions)} of {len(mmsi_list)} rigs in 5 minutes")
    print(f"Results written to {out_path}")


if __name__ == "__main__":
    main()
