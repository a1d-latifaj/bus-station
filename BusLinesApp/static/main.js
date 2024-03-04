// main.js
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const wsPath = wsProtocol + window.location.host + '/ws/vehicle_updates/';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/navigation-night-v1',
    center: [0, 0], // Default center
    zoom: 9 // Default zoom
});

const vehicleMarker = new mapboxgl.Marker()
    .setLngLat([0, 0])
    .addTo(map);

const ws = new WebSocket(wsPath);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const { latitude, longitude } = data.position;
    
    vehicleMarker.setLngLat([longitude, latitude]);
    map.flyTo({ center: [longitude, latitude] });
};
