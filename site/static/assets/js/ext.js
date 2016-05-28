function NormalDensityZx(x, Mean, StdDev) {
  var a = x - Mean;
  return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev);
}

function GenerateChartData(mean_0, stddev_0, mean_1, stddev_1) {
  var chartData = new Array([]);
  var index = 0;
  var lower_limit = Math.min(mean_0 - 3*stddev_0, mean_1 - 3*stddev_1);
  var upper_limit = Math.max(mean_0 + 3*stddev_0, mean_1 + 3*stddev_1);

  for (var i = lower_limit; i < upper_limit; i += 0.1) {
    chartData[index] = new Array(3);
    chartData[index][0] = i;
    chartData[index][1] = NormalDensityZx(i, mean_0, stddev_0);
    chartData[index][2] = NormalDensityZx(i, mean_1, stddev_1);
    index++;
  }
  return chartData;
}

function drawIndCommChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Electricity Usage');
  data.addColumn('number', 'Individual');
  data.addColumn('number', 'Community');

  data.addRows(GenerateChartData(ind_mean,ind_stddev,comm_mean,comm_stddev));

  options = { legend: 'bottom' };
  options.hAxis = {};
  options.hAxis.minorGridlines = {};
  options.hAxis.minorGridlines.count = 12;

  var chart = new google.visualization.AreaChart(document.getElementById('ind_comm'));

  chart.draw(data, options);
}

function drawIndNatChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Electricity Usage');
  data.addColumn('number', 'Individual');
  data.addColumn('number', 'National');

  data.addRows(GenerateChartData(ind_mean,ind_stddev,national_mean,national_stddev));

  options = { legend: 'bottom' };
  options.hAxis = {};
  options.hAxis.minorGridlines = {};
  options.hAxis.minorGridlines.count = 12;

  var chart = new google.visualization.AreaChart(document.getElementById('ind_national'));

  chart.draw(data, options);
}

google.load('visualization', '1', { packages: ['corechart'], callback: drawIndCommChart });

google.load('visualization', '1', { packages: ['corechart'], callback: drawIndNatChart });

$(function () {
  $('#energy-form').parsley().on('field:validated', function() {
    console.log($('.parsley-error'));
    var ok = $('.parsley-error').length === 0;
    $('.bs-callout-info').toggleClass('hidden', !ok);
    $('.bs-callout-warning').toggleClass('hidden', ok);
  })
});

$(document).ready(function(){
    $(".dollar-input").wrap('<span class="dollar">');
});
