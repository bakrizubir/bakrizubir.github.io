---
layout: default
title: Offshore Rig Tracker
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

# Offshore Rig Tracker

<div style="background-color: #f4f4f4; border-left: 4px solid #0066cc; padding: 20px; margin: 20px 0; border-radius: 5px;">
This map shows approximate positions of offshore drilling rigs sourced from public AIS (Automatic Identification System) broadcasts and industry tracking data. Positions are updated periodically — rigs that have disabled their transponders or are in transit may not appear. Not all active rigs are included.
</div>

<div id="rig-map" style="height: 500px; width: 100%; border-radius: 5px; margin: 20px 0;"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var map = L.map('rig-map').setView([20, 60], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
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

var rigs = [
  { name: 'Al Hoda',               type: 'jackup', operator: 'Bapco / ABAN',       depth: '300 ft',   status: 'Active', lat:  26.22, lng:  50.48, field: 'Bahrain Field' },
  { name: 'West Castor',           type: 'jackup', operator: 'Seadrill',            depth: '375 ft',   status: 'Active', lat:  27.10, lng:  49.60, field: 'Arabian Gulf' },
  { name: 'West Capella',          type: 'semi',   operator: 'Seadrill',            depth: '10,000 ft',status: 'Active', lat:   4.85, lng: 112.95, field: 'Sarawak, Malaysia' },
  { name: 'ENSCO 55',              type: 'jackup', operator: 'Valaris',             depth: '350 ft',   status: 'Active', lat:   9.80, lng: 100.90, field: 'Gulf of Thailand' },
  { name: 'Atwood Orca',           type: 'drill',  operator: 'Valaris',             depth: '12,000 ft',status: 'Active', lat:   8.10, lng: 107.20, field: 'Offshore Vietnam' },
  { name: 'Paul B. Loyd Jr.',      type: 'semi',   operator: 'Transocean',          depth: '1,500 ft', status: 'Active', lat:  60.30, lng:   1.20, field: 'UK North Sea' },
  { name: 'Deepsea Aberdeen',      type: 'semi',   operator: 'Odfjell Drilling',    depth: '5,000 ft', status: 'Active', lat:  58.50, lng:   1.80, field: 'UK North Sea' },
  { name: 'Deepwater Invictus',    type: 'drill',  operator: 'Transocean',          depth: '12,000 ft',status: 'Active', lat:  27.40, lng: -89.80, field: 'Gulf of Mexico' },
  { name: 'Valaris DS-11',         type: 'drill',  operator: 'Valaris',             depth: '12,000 ft',status: 'Active', lat:  28.10, lng: -88.50, field: 'Gulf of Mexico' },
  { name: 'Topaz Driller',         type: 'jackup', operator: 'Vantage Drilling',    depth: '375 ft',   status: 'Active', lat:  16.50, lng:  94.50, field: 'Offshore Myanmar' },
];

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
