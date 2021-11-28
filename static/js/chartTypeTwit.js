// <!-- Тип твита -->
var options = {
    series: [{
        name: "Количество",
        data: []//[1380, 1222, 623, 581, 223]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartTypeTwit",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true
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
        categories: ['Reply', 'Retweet', 'Self-Reply', 'Quote', 'Tweet'],
        labels: {
            show: false
        }
    }
};

var chartTypeTwit = new ApexCharts(document.querySelector("#chartTypeTwit"), options);
chartTypeTwit.render();