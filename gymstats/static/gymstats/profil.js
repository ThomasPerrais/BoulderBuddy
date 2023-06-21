import * as chartJs from 'https://cdn.jsdelivr.net/npm/chart.js@4.3.0/auto/+esm'


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


// $(".progress").each(function(){
    
//     var $bar = $(this).find(".bar");
//     var $val = $(this).find("span");
//     var perc = parseInt($val.text(), 10);
//     $({p:0}).animate({p:perc}, {
//       duration: 3000,
//       easing: "swing",
//       step: function(p) {
//         $bar.css({
//           transform: "rotate("+ (45+(p*1.8)) +"deg)", // 100%=180° so: ° = % * 1.8
//           // 45 is to add the needed rotation to have the green borders at the bottom
//         });
//         $val.text(p|0);
//       }
//     });
//   });


var defaultOptions = {
    responsive: true,
    plugins: {
        labels: {
            render: "value"
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

    new chartJs.Chart(ctx, {
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
