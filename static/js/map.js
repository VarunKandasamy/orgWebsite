/* ============================================================
   DEMOPOLIS COALITION — MAP JS
   Leaflet init + gold chapter markers
   ============================================================ */

(function () {
  'use strict';

  function initMap() {
    const mapEl = document.getElementById('chapters-map');
    if (!mapEl) return;

    // Chapter data injected by Jinja2 into the page
    const chapterLocations = window.CHAPTER_LOCATIONS || [];

    // Initialize Leaflet map
    const map = L.map('chapters-map', {
      center: [38.5, -90],
      zoom: 4,
      scrollWheelZoom: false,
    });

    // CartoDB Positron tiles — clean, institutional
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
    }).addTo(map);

    // Custom gold divIcon
    function makeMarker() {
      return L.divIcon({
        className: '',
        html: '<div class="chapter-marker"></div>',
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, -12],
      });
    }

    // Add markers
    chapterLocations.forEach(function (chapter) {
      const marker = L.marker([chapter.lat, chapter.lng], {
        icon: makeMarker(),
        title: chapter.name,
      });

      const popupContent = `
        <div class="popup__name">${chapter.name}</div>
        <div class="popup__location">${chapter.city}, ${chapter.state}</div>
        <div class="popup__description">${chapter.description}</div>
      `;

      marker.bindPopup(popupContent, { maxWidth: 260 });
      marker.addTo(map);
    });
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
  } else {
    initMap();
  }
})();
