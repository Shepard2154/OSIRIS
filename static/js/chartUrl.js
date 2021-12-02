// <!-- Url -->
var options = {
    series: [{
        name: "Количество",
        data: [2003, 52, 38, 23, 12, 11, 6]
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
        categories: ['twitter.com', 'iwillvote.com;', 'www.pscp.tv', 'iwillvote.com', 'joe.link', 'IWillVote.com;', 'JoeBiden.com'],
        labels: {
            show: false
        }
    }
};

var chartUrl = new ApexCharts(document.querySelector("#chartUrl"), options);
chartUrl.render();