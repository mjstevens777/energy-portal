var map;

function normalize(x, mn, mx) {
  var out = (x - mn) / (mx - mn);
  if (out < 0) out = 0;
  if (out > 1) out = 1;
  return out
}

function scaleBetween(x, mn, mx) {
  return x * (mx - mn) + mn;
}

function setStyle() {
  map.data.setStyle(function(feature) {
  	var el = feature.getProperty('elec_mean');

  	el = normalize(el, 7.6, 8.0);

    var color;
    var opacity;
    var zIndex;

	var hue = scaleBetween(el, 240.0, 0.0);
	var lightness = scaleBetween(el, 50.0, 50.0);
	var saturation = scaleBetween(el, 100.0, 100.0);

	var opacity = 0.8;
	var fillOpacityFactor = 0.3;
    var color = 'hsl(' + hue + ', ' + saturation + '%, ' + lightness + '%)';

    return {
      fillColor: color,
      strokeColor: color,
      strokeWeight: 1,
      fillOpacity: opacity * fillOpacityFactor,
      strokeOpacity: opacity,
      zIndex: zIndex
    };
  });
}

function initMap() {
    map = new google.maps.Map(document.getElementById('community-map'), {
    zoom: 4,
    center: {lat: 40, lng: -98}
  });

  // NOTE: This uses cross-domain XHR, and may not work on older browsers.
  map.data.loadGeoJson('static/assets/json/electricity.geojson');

  var infowindow = new google.maps.InfoWindow({
    content: ""
  });

  map.data.addListener('click', function(event) {
    var feature = event.feature;
    var el = feature.getProperty('elec_mean');
    var std = feature.getProperty('elec_std');
    var usage = Math.exp(el).toFixed(0);
    var pct_var = (1 - Math.exp(- std )) * 100;
    html = '' + usage + ' kWh<br>&plusmn;' + pct_var.toFixed(0) + '%';

    infowindow.setContent(html);
    infowindow.setPosition(event.latLng);
    infowindow.open(map);
  });

  setStyle();
}

