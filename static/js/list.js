// generate 300 random points features
const getRandomNumber = function (min, ref) {
    return Math.random() * ref + min;
}
const features = [];
for (i = 0; i < 300; i++) {
    features.push(new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([
            -getRandomNumber(50, 50), getRandomNumber(10, 50)
        ]))
    }));
}
// create the source and layer for random features
const vectorSource = new ol.source.Vector({
    features
});
const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: new ol.style.Style({
        image: new ol.style.Circle({
            radius: 2,
            fill: new ol.style.Fill({ color: 'red' })
        })
    })
});
// create map and add layers
const map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
        vectorLayer
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([-75, 35]),
        zoom: 2
    })
});

// change position of the first point
// features[0].getGeometry().setCoordinates(ol.proj.fromLonLat([2.606256612671855, 48.58965113155908]));

// Ajouter un écouteur pour l'événement change:center
map.getView().on('change:center', function (event) {
    features[0].getGeometry().setCoordinates(event.target.getCenter());
});

map.getView().on('pointerdrag', function (event) {
    features[0].getGeometry().setCoordinates(event.target.getCenter());
});
