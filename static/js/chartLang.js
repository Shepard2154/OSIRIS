// <!-- Интерфейс -->
var options = {
    series: [{
        name: "Количество",
        data: [3216, 21, 9, 2, 1, 1]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartLang",
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
        categories: ['en', 'es', 'und', 'fr', 'pt', 'tr'],
        labels: {
            show: false
        }
    }
};

var chartLang = new ApexCharts(document.querySelector("#chartLang"), options);
chartLang.render();