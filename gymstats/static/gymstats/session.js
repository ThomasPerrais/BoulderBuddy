import * as chartJs from 'https://cdn.jsdelivr.net/npm/chart.js@4.3.0/auto/+esm'

import { colorMap } from "./colors.js";

const summaryTags = document.querySelector(".summary")


let emojis = ["&#128557;", "&#128546;", "&#128534;",
 "&#128530;", "&#128528;", "&#128522;", "&#128513;",
  "&#128526;", "&#129321;", "&#128525;"];


const ProblemsOutcome = {
    Successes: Symbol("success"),
    Fails: Symbol("fail"),
    Zones: Symbol("zone"),
    All: Symbol("all")
}


let sessData = JSON.parse(document.getElementById('sessData').textContent);


function createDiagonalPattern(color) {
    let shape = document.createElement('canvas')
    shape.width = 10
    shape.height = 10
    let c = shape.getContext('2d')
    c.strokeStyle = color
    c.beginPath()
    c.moveTo(2, 0)
    c.lineTo(10, 8)
    c.stroke()
    c.beginPath()
    c.moveTo(0, 8)
    c.lineTo(2, 10)
    c.stroke()
    return c.createPattern(shape, 'repeat')
}


const drawRadarMultiple = (pbData, options, successOnly) => {
    let ctx = getCtx(pbData),
        [labels, dataSuccess, dataFail, colors] = formatDataMultiple(pbData);

    let dataAll = [];
    for(var i = 0; i < dataSuccess.length; i++){
        dataAll.push(dataSuccess[i] + dataFail[i]);
    }

    let datasets = [{
        label: 'Problem ' + pbData + ' (All)',
        data: dataAll,
        fill: true,
        backgroundColor: '#c692db53',
        borderColor: '#c692db',
        pointBackgroundColor: '#c692db',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#c692db'
    }, {
        label: 'Problem ' + pbData + ' (Success)',
        data: dataSuccess,
        fill: true,
        backgroundColor: '#9bdb9253',
        borderColor: '#98db92',
        pointBackgroundColor: '#98db92',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#98db92'
    }];
    if (!successOnly) {
        datasets.push({
            label: 'Problem ' + pbData + ' (Fail)',
            data: dataFail,
            fill: true,
            backgroundColor: '#db92a953',
            borderColor: '#db92a1',
            pointBackgroundColor: '#db92a1',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#db92a1'
        });
    }

    new chartJs.Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: options
    })
}

const drawBar = (pbData, options, outcome) => {
    let ctx = getCtx(pbData),
        [labels, data, colors] = formatData(pbData, outcome);
    new chartJs.Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: 'Problem ' + pbData,
                backgroundColor: colors,
                data: data,
                borderRadius: 10
            }]
        },
        options: options
    });
}


const drawBarMultiple = (pbData, options) => {
    let ctx = getCtx(pbData),
        [labels, dataSuccess, dataFail, colors] = formatDataMultiple(pbData);
    
    // for transparency
    let a = "a0";
    let colorsMiddle = [];
    colors.forEach(c => {
        colorsMiddle.push(createDiagonalPattern(c));
    });
    
    new chartJs.Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: 'Problem ' + pbData + ' (Top)',
                backgroundColor: colors,
                data: dataSuccess,
                barPercentage: 0.6
            }, {
                label: 'Problem ' + pbData + ' (Fail)',
                backgroundColor: colorsMiddle,
                borderColor: colors,
                borderWidth: 2,
                data: dataFail,
                barPercentage: 0.6
            }
        ]},
        options: options
    });
}


const drawRadar = (pbData, options, outcome) => {
    let ctx = getCtx(pbData),
        [labels, data, colors] = formatData(pbData, outcome);
    new chartJs.Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: [{
                label: 'Problem ' + pbData,
                data: data,
                fill: true,
                backgroundColor: '#c692db53',
                borderColor: '#c692db',
                pointBackgroundColor: '#c692db',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#c692db'
            }]
        },
        options: options
    });
}


const drawPie = (pbData, options, outcome, type="doughnut") => {
    let ctx = getCtx(pbData),
        [labels, data, colors] = formatData(pbData, outcome);

    new chartJs.Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Problem ' + pbData,
                backgroundColor: colors,
                data: data
            }]
        },
        options: options
    });
}


function formatData(pbData, outcomes) {
    let colors = [],
    labels = [],
    data = [];

    let rawData = sessData["problems"][pbData];
    for (var elt in rawData) {
        labels.push(elt);
        switch (outcomes) {
            case ProblemsOutcome.All:
                data.push(rawData[elt][0] + rawData[elt][1]);
                break;
            case ProblemsOutcome.Successes:
                data.push(rawData[elt][0]);
                break;
            case ProblemsOutcome.Fails:
                data.push(rawData[elt][1]);
                break;
        }
        colors.push(elt in colorMap ? colorMap[elt]: "black");
    }

    return [labels, data, colors];
} 


function formatDataMultiple(pbData) {
    let colors = [],
    labels = [],
    dataSuccess = [],
    dataFail = [];

    let rawData = sessData["problems"][pbData];
    for (var elt in rawData) {
        labels.push(elt);
        dataFail.push(rawData[elt][1]);
        dataSuccess.push(rawData[elt][0]);
        colors.push(elt in colorMap ? colorMap[elt]: "");
    }

    return [labels, dataSuccess, dataFail, colors];
} 


function getCtx(pbData) {
    var $types = $("#pb-" + pbData);
    return $types[0].getContext("2d");
}


var defaultOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'right',
            display: false
        }
    }
};

// Problems Types
drawPie("types", defaultOptions,  ProblemsOutcome.All);

// Problems Grades
let barMultiOpts = {
    responsive: true,
    plugins: {
        legend: {
            position: 'right',
            display: false
        }
    },
    scales: {
        x: {
            stacked: true,
            grid: {
                display: false
            }
        },
        y: {
            stacked: true,
            ticks: {
                stepSize: 1
            }

        }
    }
}
drawBarMultiple("grades", barMultiOpts,  ProblemsOutcome.All);

// Problems Holds
let radarOpts = {
    responsive: true,
    plugins: {
        legend: {
            position: 'right',
            display: false
        }
    },
    scales: {
        r: {
            beginAtZero: true,
            min: 0,
            ticks: {
                stepSize: 1
            }
        }

    }
};

// drawRadar("holds", radarOpts, ProblemsOutcome.All);
drawRadarMultiple("holds", radarOpts, true);


const renderEmojis = () => {

    let hour = Math.floor(sessData["duration"]),
    minutes = Math.ceil((sessData["duration"] - hour) * 60);
    if (minutes % 10 == 1 || minutes % 10 == 6){
        minutes = minutes - 1
    }

    let divTag = "";
    // adding time:
    divTag += `<div class="col"><center class="emoji">&#128337;</center><center>${hour}h${minutes}</center></div>`
    // adding grade
    divTag += `<div class="col"><center class="emoji">${emojis[sessData["grade"]]}</center><center>${sessData["grade"] + 1}/10</center></div>`
    // adding successes
    divTag += `<div class="col"><center class="emoji">&#128170;</center><center>${sessData["successes"]}%</center></div>`
    summaryTags.innerHTML = divTag
}
renderEmojis();

