var options = {
    series: {
        lines: {
            show: false
        },
        points: {
            show: true,
            radius: 4
        },
        splines: {
            show: true,
            tension: 0.4,
            lineWidth: 1,
            fill: 0.5
        }
    },
    grid: {
        borderColor: '#eee',
        borderWidth: 1,
        hoverable: true,
        backgroundColor: '#fcfcfc'
    },
    tooltip: true,
    tooltipOpts: {
        content: function (label, x, y) { return x + ' : ' + y; }
    },
    xaxis: {
        tickColor: '#fcfcfc',
        mode: 'categories'
    },
    yaxis: {
        min: 0,
        tickColor: '#eee',
        //position: 'right' or 'left',
        tickFormatter: function (v) {
            return v/* + ' visitors'*/;
        }
    },
    shadowSize: 0
};