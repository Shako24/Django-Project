// Initialize and add the map
function initMap() {
    // textbox used to return lat lng of the marker set by user
    const latLngInput = document.getElementById("id_lat_lng");

    // The location of previously saved marker, if exists
    const markerPosition = { lat: parseFloat("{{ mLat }}"), lng: parseFloat("{{ mLng }}") };

    // The location of dubai
    let startPosition = { lat: 25.2048, lng: 55.2708 };

    // Checking if marker set previously. If set, init map and form accordingly
    if (parseInt("{{ mLat }}") != 0) {
        startPosition = markerPosition;
        latLngInput.value = "({{ mLat }}, {{ mLng }})";
    }

    // The map, centered at dubai
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: startPosition,
    });

    // Create an info window to share between markers.
    const infoWindow = new google.maps.InfoWindow();

    // Creating init marker, and setting location if previously saved marker location exists
    let marker = null;
    if (parseInt("{{ mLat }}") != 0) {
        marker = new google.maps.Marker({
            position: markerPosition,
            map: map,
            optimized: false,
        });
    }

    // Reference for adding marker onclick: https://stackoverflow.com/questions/15792655/add-marker-to-google-map-on-click
    google.maps.event.addListener(map, 'click', function (event) {
        if (marker != null) {
            marker.setMap(null);
        }
        marker = new google.maps.Marker({
            position: event.latLng,
            map: map,
            optimized: false,
        });
        latLngInput.value = event.latLng;
        // Add a click listener for each marker, and set up the info window.
        marker.addListener("mouseover", () => {
            infoWindow.close();
            infoWindow.setContent("{{ display }}" + event.latLng);
            infoWindow.open(marker.getMap(), marker);
        });
        marker.addListener("mouseout", () => {
            infoWindow.close();
        });
    });
}
// Creating the map
window.initMap = initMap;
