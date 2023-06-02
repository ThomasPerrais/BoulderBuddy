
let stats = JSON.parse(document.getElementById('stats').textContent);
const statsTags = document.querySelectorAll(".statistics");
const btnShowStats = document.querySelector(".show-stats");

let attrKeys = {"ty": "Type", "hh": "Handhold", "fw": "Footwork", "me": "Method"}

if (Object.keys(stats).length > 0) {
    btnShowStats.addEventListener('click', (e) => {
        
        for (let i = 0; i < statsTags.length; i++) {
            statsTags[i].style.display = "flex";
        }
        let any = false;
        for (let attr in attrKeys) {
            if (stats[attr].length > 0)
            {
                any = true;
                const attrTable = document.createElement("table");

                const title = document.createElement("tr");
                title.innerHTML = `<th>${attrKeys[attr]}</th><th>Odds Ratio</th><th>P-Value</th>`

                attrTable.appendChild(title);

                for (let i = 0; i < stats[attr].length; i++) {
                    const row = document.createElement("tr");
                    row.innerHTML = `<th>${stats[attr][i][0]}</th><th>${stats[attr][i][1].toFixed(2)}</th><th>${stats[attr][i][2].toFixed(2)}</th>`
                    attrTable.appendChild(row);
                }
                statsTags[0].appendChild(attrTable);

            }
        }
        if (!any) {
            let p = document.createElement("p");
            p.innerHTML = "no significant over-represented features were found."
            statsTags[0].appendChild(p);
        }
    });
}
else {
    btnShowStats.style.display = "none"
}

