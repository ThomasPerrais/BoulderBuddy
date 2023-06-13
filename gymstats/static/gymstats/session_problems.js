

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

let message = JSON.parse(document.getElementById('message').textContent);

function showMessage(msg, success) {
    var popup = document.getElementById("popup");
    var popupContent = document.getElementById("popup-content");
    popup.style.display = "block";
    popup.className += " " + success;
    popupContent.innerHTML = msg;
  }
  
  function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
  }

if (message["content"] != "") {
    showMessage(message["content"], message["success"]);
}