// <!-- Hash -->
var options = {
    series: [{
        name: "Количество",
        data: [4, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1, 6, 1, 2, 1, 1, 3, 1, 1, 1, 5, 1, 1, 1, 2, 1, 1]
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
        categories: ['SOULSaturday', 'TeamJoe', 'LGBTQ', 'WorldPressFreedomDay', 'TodosConBiden', 'VEDay', 'EqualityAct', 'League46', 'AB5', 'GunViolenceAwarenessDay', 'WorkersFirst', 'Juneteenth', 'DCStatehood', 'PrideMonth', 'ImmigrantHeritageMonth', 'NoBanAct', 'OpeningDay', 'CelebrationForChange', 'EidAlAdha', 'DemConvention', 'WomensEqualityDay', 'NationalDogDay', 'FabFive', 'RoshHashanah', 'BidenTownHall', 'NationalBlackVoterDay', 'NationalVoterRegistrationDay', 'OctoberVoter', 'WorldTeachersDay', 'ImVotingFor', 'IASen', 'NationalDessertDay', 'SpiritDay', 'VoteEarlyDay', 'OnlyTheYoung', 'BidenForFL', 'RockinEve', 'Inauguration2021', 'LunarNewYear', 'InternationalWomensDay'],
        labels: {
            show: false
        }
    }
};

var chartHash = new ApexCharts(document.querySelector("#chartHash"), options);
chartHash.render()