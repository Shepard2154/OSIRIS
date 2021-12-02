// <!-- Используемый язык -->
var options = {
    series: [{
        name: "Количество",
        data: [1216, 792, 741, 248, 133, 120]
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
        categories: ['TweetDeck', 'Twitter Web App', 'Twitter Media Studio', 'Sprout Social', 'Periscope', 'Twitter for iPhone'],
        labels: {
            show: false
        }
    }
};

var chartClient = new ApexCharts(document.querySelector("#chartClient"), options);
chartClient.render();