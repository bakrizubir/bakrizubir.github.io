---
layout: default
title: Spindletop™ Offshore Rig Tracker
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

# Spindletop&trade; Offshore Rig Tracker

<p style="color: #888; font-size: 0.9em; margin-top: -10px; margin-bottom: 20px;">built by Bakri Zubir</p>

<div style="background-color: #f4f4f4; border-left: 4px solid #0066cc; padding: 20px; margin: 20px 0; border-radius: 5px;">
This map will show offshore drilling rig positions tracked by IMO/MMSI via public AIS broadcasts. Live AIS integration is currently in development — rig data will populate here once the automated daily update system is live. Rig list update is ongoing..
</div>

<div id="rig-map" style="height: 750px; width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; margin-top: 20px; margin-bottom: 20px; border-radius: 0;"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var map = L.map('rig-map').setView([20, 60], 3);

L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
  maxZoom: 19,
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>'
}).addTo(map);

var rigTypes = {
  jackup: { color: '#e67e22', label: 'Jackup' },
  semi:   { color: '#0066cc', label: 'Semi-submersible' },
  drill:  { color: '#27ae60', label: 'Drillship' }
};

function makeIcon(type) {
  var c = rigTypes[type].color;
  return L.divIcon({
    className: '',
    html: '<div style="width:14px;height:14px;border-radius:50%;background:' + c + ';border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.4);"></div>',
    iconSize: [14, 14], iconAnchor: [7, 7], popupAnchor: [0, -10]
  });
}

var rigs = [];

rigs.forEach(function(rig) {
  L.marker([rig.lat, rig.lng], { icon: makeIcon(rig.type) })
    .addTo(map)
    .bindPopup(
      '<div style="font-family:sans-serif;min-width:180px;">' +
      '<strong style="color:#0066cc;">' + rig.name + '</strong><br>' +
      '<span style="color:#888;font-size:0.85em;">' + rigTypes[rig.type].label + '</span><br><br>' +
      '<table style="font-size:0.85em;width:100%;border-collapse:collapse;">' +
      '<tr><td style="color:#555;padding:2px 8px 2px 0;">Field</td><td>'       + rig.field    + '</td></tr>' +
      '<tr><td style="color:#555;padding:2px 8px 2px 0;">Operator</td><td>'    + rig.operator + '</td></tr>' +
      '<tr><td style="color:#555;padding:2px 8px 2px 0;">Water Depth</td><td>' + rig.depth    + '</td></tr>' +
      '<tr><td style="color:#555;padding:2px 8px 2px 0;">Status</td><td><span style="color:#27ae60;">● ' + rig.status + '</span></td></tr>' +
      '</table></div>'
    );
});

var legend = L.control({ position: 'bottomright' });
legend.onAdd = function() {
  var div = L.DomUtil.create('div');
  div.style.cssText = 'background:white;padding:10px 14px;border-radius:5px;box-shadow:0 1px 5px rgba(0,0,0,0.2);font-family:sans-serif;font-size:0.82em;line-height:1.8;';
  div.innerHTML =
    '<strong style="display:block;margin-bottom:4px;">Rig Type</strong>' +
    '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#e67e22;vertical-align:middle;margin-right:6px;"></span>Jackup<br>' +
    '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#0066cc;vertical-align:middle;margin-right:6px;"></span>Semi-sub<br>' +
    '<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#27ae60;vertical-align:middle;margin-right:6px;"></span>Drillship';
  return div;
};
legend.addTo(map);
</script>

---

[← Back to Home](./)
