function DiracDensity(x, Mean, StdDev) {
  return
}

function NormalDensityZx(x, Mean, StdDev) {
  var a = x - Mean;
  return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev);
}

function LogNormalDensityZx(x, Mean, StdDev) {
  var a = Math.log(x) - Math.log(Mean);
  //a = a - StdDev * StdDev; // This is a hack to get the mode of the distribution to show up at
  return Math.exp(-(a * a) / (2 * StdDev * StdDev)) / (Math.sqrt(2 * Math.PI) * StdDev);
}

function GenerateChartData(mean_0, stddev_0, density_0, mean_1, stddev_1, density_1) {
  var chartData = new Array([]);
  var index = 0;

  var lower_limit = 1000;
  // Math.max(
  //     Math.min(
  //       mean_0 * Math.exp(-3*stddev_0),
  //       mean_1 * Math.exp(-3*stddev_1)
  //     ), 0);
  var upper_limit = 40000;
  // Math.max(
  //   mean_0 * Math.exp(3*stddev_0),
  //   mean_1 * Math.exp(stddev_1)
  // );

  var step = (upper_limit - lower_limit) / 500;

  for (var i = lower_limit; i < upper_limit; i += step) {
    chartData[index] = new Array(3);
    chartData[index][0] = i;
    chartData[index][1] = density_0(i, mean_0, stddev_0);
    chartData[index][2] = density_1(i, mean_1, stddev_1);
    index++;
  }
  return chartData;
}

function drawIndCommChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Electricity Usage');
  data.addColumn('number', 'Individual');
  data.addColumn('number', 'Community');

  data.addRows(GenerateChartData(
    ind_mean, ind_stddev, LogNormalDensityZx,
    comm_mean, comm_stddev, LogNormalDensityZx
  ));

  options = { legend: 'bottom' };
  options.hAxis = {};
  options.hAxis.logScale = true;
  options.hAxis.ticks = [1000, 2000, 4000, 6000, 10000, 20000, 40000]

  var chart = new google.visualization.AreaChart(document.getElementById('ind_comm'));

  chart.draw(data, options);
}

function drawCommNatChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Electricity Usage');
  data.addColumn('number', 'Community');
  data.addColumn('number', 'National');

  data.addRows(GenerateChartData(
    comm_mean, comm_stddev, LogNormalDensityZx,
    national_mean, national_stddev, LogNormalDensityZx
  ));

  options = { legend: 'bottom' };
  options.hAxis = {};
  options.hAxis.logScale = true;
  options.hAxis.ticks = [1000, 2000, 4000, 6000, 10000, 20000, 40000]
  // options.hAxis.majorGridlines = {};
  // options.hAxis.majorGridlines.count = 4;
  // options.hAxis.minorGridlines = {};
  // options.hAxis.minorGridlines.count = 12;

  var chart = new google.visualization.AreaChart(document.getElementById('comm_national'));

  chart.draw(data, options);
}

function drawIndNatChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Electricity Usage');
  data.addColumn('number', 'Individual');
  data.addColumn('number', 'National');

  data.addRows(GenerateChartData(
    ind_mean, ind_stddev, LogNormalDensityZx,
    national_mean, national_stddev, LogNormalDensityZx
  ));

  options = { legend: 'bottom' };
  options.hAxis = {};
  options.hAxis.logScale = true;
  options.hAxis.ticks = [1000, 2000, 4000, 6000, 10000, 20000, 40000]
  // options.hAxis.majorGridlines = {};
  // options.hAxis.majorGridlines.count = 4;
  // options.hAxis.minorGridlines = {};
  // options.hAxis.minorGridlines.count = 12;

  var chart = new google.visualization.AreaChart(document.getElementById('ind_national'));

  chart.draw(data, options);
}

google.load('visualization', '1', { packages: ['corechart'], callback: drawIndCommChart });

google.load('visualization', '1', { packages: ['corechart'], callback: drawIndNatChart });

google.load('visualization', '1', { packages: ['corechart'], callback: drawCommNatChart });


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
