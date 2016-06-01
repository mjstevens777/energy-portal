var map;
var markers = [];

function initMap() {
  // Create a map object and specify the DOM element for display.
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.769, lng: -122.446},
    scrollwheel: false,
    zoom: 8 
  });

  google.maps.event.addListener(map, 'click', function(event) {
    placeMarker(event.latLng);
    var latitude = event.latLng.lat();
    var longitude = event.latLng.lng();
    console.log( latitude + ', ' + longitude );
  });

  function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

  function placeMarker(location) {
    document.getElementById("lat_span").innerHTML = location.lat();
    document.getElementById("lng_span").innerHTML = location.lng();

    document.getElementById("lat_val").value = location.lat();
    document.getElementById("lng_val").value = location.lng();
    setMapOnAll(null);
    var marker = new google.maps.Marker({
      position: location,
      map: map
    });
    markers.push(marker);
  }
}

