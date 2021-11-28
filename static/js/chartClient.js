// <!-- Используемый язык -->
var options = {
    series: [{
        name: "Количество",
        data: [2180, 822, 23]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartClient",
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
        categories: ['Twitter for Android', 'Twitter Web App', 'Twitter Web Client'],
        labels: {
            show: false
        }
    }
};

var chartClient = new ApexCharts(document.querySelector("#chartClient"), options);
chartClient.render();