// OS Chart
document.addEventListener('DOMContentLoaded', function () {

    var osNames = [];
    var osValues = [];
  
    osDataPercentages.forEach(function (item) {
        osNames.push(item.name);  // Use the name from the data
        osValues.push(item.percentage);
    });
  
  
    var staticColors = [
        '#5d65cf', '#bf3758', '#34a853', '#4285f4', '#fb8c00',
        '#9e9e9e', '#1976D2', '#009688', '#FFC107', '#E91E63',
        '#FF5722', '#673AB7', '#8BC34A', '#03A9F4', '#FFEB3B',
        '#607D8B', '#9C27B0', '#795548', '#CDDC39', '#FF9800',
        '#4CAF50', '#2196F3', '#00BCD4', '#FFEB3B'
    ];
  
    var osColors = staticColors.slice(0, osNames.length);
  
    var osChartElement = document.getElementById('osVisitorChart');
    if (!osChartElement) {
        console.error("Chart element not found. Make sure the element ID is correct.");
        return;
    }
  
    var osCtx = osChartElement.getContext('2d');
    if (!osCtx) {
        console.error("Unable to get chart context. Make sure the element ID is correct.");
        return;
    }
  
    var osChart = new Chart(osCtx, {
        type: 'doughnut',
        data: {
            labels: osNames,
            datasets: [{
                data: osValues,
                backgroundColor: osColors,
                hoverBackgroundColor: osColors,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.label || '';
                            var value = context.raw || 0;
                            return label + '\n' + value + '%';
                        }
                    }
                }
            }
        }
    });
  });
  
  
  // Browser Chart
  document.addEventListener('DOMContentLoaded', function () {
  
    var browserNames = [];
    var browserValues = [];
  
    browserDataPercentages.forEach(function (item) {
        browserNames.push(item.name);
        browserValues.push(item.percentage);
    });
  
    var staticColors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
        '#1f78b4', '#ff7f0f', '#33a02c', '#d62a29', '#9468bd',
        '#8d574b', '#e277c3', '#7e7e7e', '#bdbe22', '#18becf',
        '#afc7e8', '#ffbc79', '#99df8b', '#ff9997', '#c6b1d5',
        '#c59c95', '#f6b6d3', '#c8c8c8', '#dcdb8e', '#9fdae6',
    ];
  
    var browserColors = staticColors.slice(0, browserNames.length);
  
    var browserChartElement = document.getElementById('browserVisitorChart');
    if (!browserChartElement) {
        console.error("Chart element not found. Make sure the element ID is correct.");
        return;
    }
  
    var browserCtx = browserChartElement.getContext('2d');
    if (!browserCtx) {
        console.error("Unable to get chart context. Make sure the element ID is correct.");
        return;
    }
  
    var browserChart = new Chart(browserCtx, {
        type: 'doughnut',
        data: {
            labels: browserNames,
            datasets: [{
                data: browserValues,
                backgroundColor: browserColors,
                hoverBackgroundColor: browserColors,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            var label = context.label || '';
                            var value = context.raw || 0;
                            return label + '\n' + value + '%';
                        }
                    }
                }
            }
        }
    });
  });