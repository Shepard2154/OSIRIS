// <!-- Answers -->
var options = {
    series: [{
        name: "Количество",
        data: [31, 22, 8, 5, 3]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id: "chartAnswers",
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
        categories: ['@AnnaNews', '@KremlinRussia', '@WestPoint', '@BellingCat', "@isis"],
        labels: {
            show: false
        }
    }
};

var chartAnswers = new ApexCharts(document.querySelector("#chartAnswers"), options);
chartAnswers.render();