let message = JSON.parse(document.getElementById('message').textContent);

$(document).ready(function() {
    // Wait for the document to be fully loaded before manipulating it
    if (message["content"] != "") {

        // popup animation
        var $popup = $(this).find(".popup");
        $popup.text(message["content"]);
        $popup.addClass(message["success"]);
    
        // Show the popup
        $popup.show();
        // Delay the execution of the next function by 2 seconds
        $popup.delay(1500).fadeOut();
    }
});