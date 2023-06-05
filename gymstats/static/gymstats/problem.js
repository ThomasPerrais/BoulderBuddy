const summaryTag = document.querySelector(".summary");

const statusMap = {
    "Not Tried": "⬜",
    "Fail": "🟥",
    "Zone": "🟨",
    "Top": "🟩",
}

const colorMap = {
    "Yellow": "🟡",
    "Orange": "🟠",
    "Green": "🟢",
    "Blue": "🔵",
    "Red": "🔴",
    "Black": "⚫",
    "Purple": "🟣",
    "Gray": "💿",
    "White": "⚪",
    "Pink": "🧠",
    "B5": "🔵",
    "B6": "🔵",
    "B7": "🔴",
    "B8": "🔴",
    "B9": "⚪",
    "B10": "⚪",
    "B11": "⚫",
    "B12": "⚫",
    "B13": "🟢",
    "B14": "🟢",
};

const data = document.currentScript.dataset;
let achieved = data.status,
    grade = data.grade;

summaryTag.children[2].children[0].innerHTML = statusMap[achieved];
summaryTag.children[1].children[0].innerHTML = colorMap[grade];
summaryTag.children[1].children[1].innerHTML = grade;
