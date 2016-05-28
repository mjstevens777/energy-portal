
function drawChart() {

  var data = new google.visualization.DataTable();
  data.addColumn('number', 'You');
  data.addColumn('number', 'Community');
  data.addColumn('number', 'Electricity Usage');

  function NormalDensityZx(x, Mean, StdDev) {
    var a = x - Mean;
    return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev);
  }

  var chartData = new Array([]);
  var index = 0;

  for (var i = -3; i < 3.1; i += 0.1) {
    chartData[index] = new Array(3);
    chartData[index][0] = i;
    chartData[index][1] = NormalDensityZx(i, 0, 1);
    chartData[index][2] = NormalDensityZx(i, 0.5, 0.5);
    index++;
  }

  data.addRows(chartData);
  options = { legend: 'none' };
  options.hAxis = {};
  options.hAxis.minorGridlines = {};
  options.hAxis.minorGridlines.count = 12;

  var chart1 = new google.visualization.AreaChart(document.getElementById('ind_com'));
  var chart2 = new google.visualization.AreaChart(document.getElementById('ind_usa'));

  chart1.draw(data, options);
  chart2.draw(data, options);
}

google.load('visualization', '1', { packages: ['corechart'], callback: drawChart });

$(function () {
  $('#energy-form').parsley().on('field:validated', function() {
    console.log($('.parsley-error'));
    var ok = $('.parsley-error').length === 0;
    $('.bs-callout-info').toggleClass('hidden', !ok);
    $('.bs-callout-warning').toggleClass('hidden', ok);
  })
});

function initMap() {
  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    scrollwheel: false,
    zoom: 8
  });
}

$(document).ready(function(){    
    $(".dollar-input").wrap('<span class="dollar">');
});
