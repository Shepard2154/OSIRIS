var options = {
    series: [ {
        name: 'Нейтральное упоминание',
        data: [9, 7, 5, 8, 6, 9, 4]
      },
  {
    name: 'Положительное упоминание',
    data: [44, 55, 41, 37, 22, 43, 21]
  }, {
    name: 'Отрицательное упоминание',
    data: [53, 32, 33, 52, 13, 43, 32]
  }],
    chart: {
    id: "chartEntity",
    type: 'bar',
    height: 2050,
    stacked: true,
    dropShadow: {
      enabled: true,
      blur: 1,
      opacity: 0.25
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '60%',
    },
  },
  
  stroke: {
    width: 0,
  },
  title: {
    text: 'Сущности и отношение к ним ЦА'
  },
  xaxis: {
    categories: ["WestPoint", "Putin", "Covid-19", "Army", "USA", "lol", "kek"]
  },
  yaxis: {
    labels:{
        show:true,
        style: {
            fontSize: '22px',
            fontWeight: 'bold',
          },
    },
    title: {
      text: undefined
    },
  },
  tooltip: {
    shared: false,
    y: {
      formatter: function (val) {
        return val + " упоминаний"
      }
    }
  },
//   fill: {
//     type: 'pattern',
//     opacity: 1,
//     pattern: {
//       style: ['circles', 'slantedLines'], // string or array of strings
  
//     }
//   },
  states: {
    hover: {
      filter: 'none'
    }
  },
  legend: {
    position: 'right',
    offsetY: 40
  }
  };

    var chartEntity = new ApexCharts(document.querySelector("#chartEntity"), options);
    chartEntity.render();


