var map = L.map('map').setView([8.325744369513515, 77.87277435423326], 50);

  // Add a tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(map);

  // Add a marker
  var marker = L.marker([8.325744369513515, 77.87277435423326]).addTo(map);