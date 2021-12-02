// <!-- Retweet -->
var options = {
    series: [{
        name: "Количество",
        data: [1, 1, 1, 1, 1, 1, 1, 5]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartRetweet",
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
        categories: ['staceyabrams', 'springsteen', 'nowthisnews', 'johnlegend', 'ewarren', 'ericswalwell', 'cindymccain', 'WhiteHouse'],
        labels: {
            show: false
        }
    }
};

var chartRetweet = new ApexCharts(document.querySelector("#chartRetweet"), options);
chartRetweet.render();