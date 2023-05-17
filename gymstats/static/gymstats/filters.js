let filters = JSON.parse(document.getElementById('filters').textContent);
const buttons = document.querySelectorAll(".add-btn");
const filterLists = document.querySelectorAll(".filter-list");

const comparers = {"eq": "", "lt": "<", "lte": "<=", "gt": ">", "gte": ">=" };

const parseFilters = () => {
    
    if ("grade" in filters) {
        for (let comp in comparers) {
            if (comp in filters["grade"]) {
                for (let i = 0; i < filters["grade"][comp].length; i++) {
                    addFilterToList(filterLists[0], comparers[comp] + filters["grade"][comp][i]);
                }
            }
        }
    }

    if ("gym" in filters) {
        for (let i = 0; i < filters["gym"]["eq"].length; i++) {
            addFilterToList(filterLists[1], filters["gym"]["eq"][i]);
        }
    }

    let attrNames = {"handhold": "hh", "footwork": "fw", "method": "me", "type": "ty"};
    for (let key in attrNames) {
        if (key in filters) {
            for (let i = 0; i < filters[key]["eq"].length; i++) {
                addFilterToList(filterLists[2], filters[key]["eq"][i], attrNames[key]);
            }
        }
    }
     // TODO: handle removed, date
}


const addFilterToList = (list, text, className="") => {
    const newLi = document.createElement("li");
    if (className != "") {
        newLi.className = className;
    }

    const xSpan = document.createElement("span");
    xSpan.className = "close";
    xSpan.innerHTML = "x";
    xSpan.onclick = () => {
        xSpan.parentElement.style.display = "none";
    }

    newLi.innerHTML = text;
    newLi.appendChild(xSpan);
    list.appendChild(newLi);
}

const linkToFilterList = (button, list, allowPrefix) => {
    
    button.addEventListener('click', (e) => {
        const newLi = document.createElement("li");
        
        const newI = document.createElement("i");
        newI.contentEditable = true;
        newI.className = "editable";

        const xSpan = document.createElement("span");
        xSpan.className = "close";
        xSpan.innerHTML = "x";

        newI.onkeydown = function(ee) {
            // TODO: remove text when first click inside <i>
            if (ee.keyCode == 13) {

                let text = newI.innerHTML,
                    cl = "";
                if (allowPrefix) {
                    const parts = text.split(':');
                    if (parts.length == 2) {
                        cl = parts[0];
                        text = parts[1];
                    }
                }

                newLi.innerHTML = text;
                newLi.className = cl;
                newLi.appendChild(xSpan);
                xSpan.onclick = () => {
                    xSpan.parentElement.style.display = "none";
                }
            }
        };

        newLi.appendChild(newI);
        newLi.appendChild(xSpan);
        list.appendChild(newLi);
    });
};


parseFilters();

for (let i = 0; i < buttons.length; i++) {
    linkToFilterList(buttons[i], filterLists[i], i == 2);
};