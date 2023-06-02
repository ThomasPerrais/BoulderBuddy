const summaryTag = document.querySelector(".summary");

const statusMap = {
    "Not Tried": "⬜",
    "Fail": "🟥",
    "Zone": "🟨",
    "Top": "🟩",
}

const colorMap = {
    "Green": "#64e059",
    "Blue": "#77adea",
    "Red": "#eb4545",
    "Black": "#353535",
    "Purple": "#b739c2",
    "B5": "#77adea",
    "B6": "#77adea",
    "B7": "#eb4545",
    "B8": "#eb4545",
    "B9": "#353535",  // here we need B9 and B10 to be black...
    "B10": "#353535",
    "B11": "#353535",
    "B12": "#353535",
    "B13": "#64e059",
    "B14": "#64e059",
};

const data = document.currentScript.dataset;
let achieved = data.status,
    grade = data.grade;

summaryTag.children[2].children[0].innerHTML = statusMap[achieved];

let gradeElt = summaryTag.children[1].children[0];
gradeElt.innerHTML = grade;
gradeElt.style.color = colorMap[grade];
gradeElt.style.border = "3px solid " + colorMap[grade]; 
