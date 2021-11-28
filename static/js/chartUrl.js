// <!-- Url -->
var options = {
    series: [{
        name: "Количество",
        data: [52, 23, 13]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartUrl",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
    },
    yaxis: {
        labels: {
            show: false
        }
    },
    xaxis: {
        categories: ['youtube.com', 'bit.ly', 'facebook.com'],
        labels: {
            show: false
        }
    }
};

var chartUrl = new ApexCharts(document.querySelector("#chartUrl"), options);
chartUrl.render();