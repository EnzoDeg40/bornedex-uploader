function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            console.log(position);
            showPosition(position);
        });
    }
    else {
        alert("La géolocalisation n'est pas prise en charge par votre navigateur.");
    }
}

getLocation();

function showPosition(position) {
    const latitudeInput = document.getElementById("lat");
    const longitudeInput = document.getElementById("lon");

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
    const latitudeInput = document.getElementById("lat");
    const longitudeInput = document.getElementById("lon");

    // Convertir les coordonnées du centre en latitude/longitude
    const lonLat = ol.proj.toLonLat(center);

    // Mettre à jour les champs de coordonnées avec le centre de la vue
    latitudeInput.value = lonLat[1];
    longitudeInput.value = lonLat[0];
});

function previewImage() {
    var preview = document.getElementById('image-preview');
    var fileInput = document.getElementById('image');
    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
    };

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = '#';
        preview.style.display = 'none';
    }
}

function validateField(inputId) {
    const input = document.getElementById(inputId);
    if (input.value.trim()) {
        input.style.border = "";
        return true;
    } 
    input.style.border = "2px solid red";
    console.warn(`Submit form: ${inputId} is empty`);
    return false;
}

document.getElementById('gpsForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    let can_submit = true;
    
    can_submit = validateField("lat") && can_submit;
    can_submit = validateField("lon") && can_submit;
    can_submit = validateField("image") && can_submit;

    if (!can_submit)
    {
        console.error("Submit form: some fields are empty");
        alert("L'altitude et la longitude et l'image sont obligatoires");
        return;
    }

    e.preventDefault();
    var formData = new FormData(this);
    fetch('/upload/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('message').innerText = data.error;
            } else {
                document.getElementById('message').innerText = data.success;
                // alert(data.success);
                // this.reset();
                // document.getElementById('image-preview').style.display = 'none';
            }
        });
});