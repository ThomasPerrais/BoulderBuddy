
function showGraphics(evt, statsName) {
    // hide 'statstab'
    let statstab = document.querySelectorAll(".statstab");
    for (let i = 0; i < statstab.length; i++) {
        statstab[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    let tablinks = document.querySelectorAll(".tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(statsName).style.display = "block";
    evt.currentTarget.className += " active";
}

var btns = document.querySelectorAll(".tablinks");
for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function(e) {
        var id = $(this).data("id");
        showGraphics(e, id);
    });
}

document.getElementById("defaultOpen").click();