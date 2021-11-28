// <!-- Hash -->
var options = {
    series: [{
        name: "Количество",
        data: [113, 87, 42, 12]
    }],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartHash",
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
        categories: ['@GodSaveAmerica', '@FuckinNigers', '@LoveRussia', '@RussianHackers'],
        labels: {
            show: false
        }
    }
};

var chartHash = new ApexCharts(document.querySelector("#chartHash"), options);
chartHash.render()