//Дни недели
var options = {
    series: [378, 401, 559, 504, 512, 506, 393],
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartDayOfWeek",
        width: '100%',
        type: 'pie',
    },
    labels: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
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