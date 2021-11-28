//Дни недели
var options = {
    series: [25, 15, 44, 41, 55, 17, 82],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartDayOfWeek",
        width: '100%',
        type: 'pie',
    },
    labels: ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    theme: {
        monochrome: {
            enabled: true
        }
    },
    title: {
        text: ""
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};

var chartDayOfWeek = new ApexCharts(document.querySelector("#chartDayOfWeek"), options);
chartDayOfWeek.render();