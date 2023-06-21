let data = JSON.parse(document.getElementById('data').textContent);

const animalEmoji = ["🦥", "🐨", "🐈‍⬛", "🐆", "🐅", "🐒", "🦧", "🦍"]

const map = {
    "time": ["duration_human_readable", "training_time_target", "lime"],
    "tops": ["hard_tops", "hard_boulders_target", "aqua"]
}

$(".progress").each(function(){

    var className = $(this).attr("class").split(" ")[1];

    // adding values to the bottom text
    var $text = $(this).find(".btm-text")
    $text.append(data["month"][map[className][0]]);

    // calculating stroke-dashoffset
    var percentage = data["month"][map[className][1]];
    var skOff = 5.65 * (100 - percentage); 

    // animal emoji
    if (className == "tops") {
        var pos = Math.floor(percentage / 12.51);
        var $centerTxt = $(this).find(".center-image");
        $centerTxt.html(animalEmoji[pos]);
    }
    
    // bar animation
    var $bar = $(this).find(".progress-bar");
    $bar.css({
        stroke: map[className][2]
    })
    $bar.animate(
        {
            "stroke-dashoffset": skOff
        },
        2000, // animation duration in milliseconds
    );
  });

const renderAllTimeInfo = () => {
    const allTime = document.querySelector(".all-time");
    let keys = {
        "duration_human_readable": "&#128337;",
        "sessions": "🧗‍♂️"
    };
    for (let key in keys) {
        // do something for each key in the object
        let div = document.createElement("div");
        div.className = "col";
        let p1 = document.createElement("p");
        p1.className = "emoji";
        p1.innerHTML = keys[key];
        let p2 = document.createElement("p");
        p2.innerHTML = data["all_time"][key];
        if (key == "sessions") {
            p2.innerHTML += " sessions"
        }
        p2.style.textAlign = "center";
        div.appendChild(p1);
        div.appendChild(p2);
        allTime.appendChild(div); 
      }
}
renderAllTimeInfo();


var defaultOptions = {
    responsive: true,
    plugins: {
        labels: {
            render: 'percentage',
            fontColor: '#000',
            fontSize: 12,
            fontStyle: 'bold'
        },
        legend: {
            position: 'right',
            display: true
        }
    }
};

let achievementProblemlabels = ["flash", "top", "zone", "fail"],
achievementProblemColors = ["#5cf311", "#d2f499", "#f3da5e", "#f39e5e"];

const drawPbPie = (ctx, prefix, options) => {
    
    let pbData = [];
    achievementProblemlabels.forEach(l => {
        pbData.push(data["year"]["pb_" + prefix + "_" + l]);
    });

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: achievementProblemlabels,
            datasets: [{
                label: 'All Problems',
                backgroundColor: achievementProblemColors,
                data: pbData
            }]
        },
        options: options
    });
}

var prefixes = ["all", "lower", "expect", "higher", "unk"]
for (let i = 0; i < prefixes.length; i++) {
    var $types = $("#year-" + prefixes[i] + "-problems");
    var ctx = $types[0].getContext("2d");
    drawPbPie(ctx, prefixes[i], defaultOptions);
}


// gym stats
var gymSelect = document.querySelector(".gym-select");
for (let key in data["by_gym"]) {
    let opt = document.createElement("option");
    opt.value = key;
    opt.text = key;
    gymSelect.appendChild(opt);
}

var $gymStats = $("#gym-stats");
var ctx = $gymStats[0].getContext("2d");

// Attach event listener to the select element
gymSelect.addEventListener('change', function(event) {
    // Get the selected option
    var selectedGym = event.target.value;
    
    // Clear the existing chart, if any
    if (window.GymChart) {
        window.GymChart.destroy();
    }

    if (selectedGym.length > 0) {
        gymData = data["by_gym"][selectedGym];
        window.GymChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: gymData["labels"],
                datasets: [{
                    label: 'Flash',
                    backgroundColor: achievementProblemColors[0],
                    data: gymData["flash"],
                    barPercentage: 0.6
                }, {
                    label: 'Top',
                    backgroundColor: achievementProblemColors[1],
                    data: gymData["top"],
                    barPercentage: 0.6
                }, {
                    label: 'Zone',
                    backgroundColor: achievementProblemColors[2],
                    data: gymData["zone"],
                    barPercentage: 0.6
                }, {
                    label: 'Fail',
                    backgroundColor: achievementProblemColors[3],
                    data: gymData["fail"],
                    barPercentage: 0.6
                }, {
                    label: 'Not Tried',
                    backgroundColor: "white",
                    borderColor: "black",
                    borderWidth: 1,
                    data: gymData["not tried"],
                    barPercentage: 0.6
                }
            ]},
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                        display: true
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
        });
    }
});


