// <!-- Цитирование -->
var options = {
    series: [{
        name: "Количество",
        data: [13, 6]
    }],
    noData: {
        text: ''
    },
    chart: {
        id:"chartQuotes",
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
        categories: ['@professor', '@KremlinRussia'],
        labels: {
            show: false
        }
    }
};

var chartQuotes = new ApexCharts(document.querySelector("#chartQuotes"), options);
chartQuotes.render();