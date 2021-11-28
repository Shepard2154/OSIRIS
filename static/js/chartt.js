var options = {
    series: [{
        name: 'Количество твитов',
        data: [254, 287, 258, 266, 283, 305, 233, 261, 254, 313, 252, 318, 251, 287, 276, 247, 239, 297, 287, 308, 273, 308, 301, 263, 311, 234, 274, 319, 280, 232, 250, 293]
    }],

    annotations: {

    },
    noData: {
        text: 'Не найдено...'
    },
    chart: {
        id:"chartt",
        height: 350,
        type: 'area',
    },

    dataLabels: {
        enabled: false
    },
    stroke: {
        width: 2
    },

    grid: {
        row: {
            colors: ['#fff', "#f2f2f2"]
        }
    },
    xaxis: {
        labels: {
            rotate: -45
        },
        categories: ["20.янв", "21.янв", "22.янв", "23.янв", "24.янв", "25.янв", "26.янв", "27.янв", "28.янв", "29.янв", "30.янв", "31.янв", "01.фев", "02.фев", "03.фев", "04.фев", "05.фев", "06.фев", "07.фев", "08.фев", "09.фев", "10.фев", "11.фев", "12.фев", "13.фев", "14.фев", "15.фев", "16.фев", "17.фев", "18.фев", "19.фев", "20.фев"],
        tickPlacement: 'on'
    },
    yaxis: {
        title: {
            text: '',
        },
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'light',
            type: "horizontal",
            shadeIntensity: 0.25,
            gradientToColors: undefined,
            inverseColors: true,
        },
    }
};

var chartt = new ApexCharts(document.querySelector("#chartt"), options);
chartt.render();