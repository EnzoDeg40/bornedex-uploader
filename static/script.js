function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else {
        alert("La géolocalisation n'est pas prise en charge par votre navigateur.");
    }
}

function showPosition(position) {
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");

    latitudeInput.value = position.coords.latitude;
    longitudeInput.value = position.coords.longitude;
    if (map.getView().getZoom() < 15) {
        map.getView().setZoom(15);
    }
    map.getView().setCenter(ol.proj.fromLonLat([position.coords.longitude, position.coords.latitude]));
}

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([2.8, 47.0016]), // [longitude, latitude]
        zoom: 6
    })
});

// Ajouter un écouteur pour l'événement change:center
map.getView().on('change:center', function (event) {
    const center = event.target.getCenter();
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");

    // Convertir les coordonnées du centre en latitude/longitude
    const lonLat = ol.proj.toLonLat(center);

    // Mettre à jour les champs de coordonnées avec le centre de la vue
    latitudeInput.value = lonLat[1];
    longitudeInput.value = lonLat[0];
});