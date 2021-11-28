// <!-- Интерфейс -->
var options = {
    series: [{
        name: "Количество",
        data: [1323, 122, 223, 81]
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
        categories: ['English', 'Undefined', 'German', 'Danish'],
        labels: {
            show: false
        }
    }
};

var chartLang = new ApexCharts(document.querySelector("#chartLang"), options);
chartLang.render();