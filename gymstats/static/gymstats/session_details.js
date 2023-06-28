
function showForm($btn) {
    let id = $btn.data("id");
    
    var $form = $(document).find(".edit-" + id);
    var $div = $(document).find(".achievement-" + id);
    
    if ($form.is(":hidden")) {
        $form.css('display', 'inline');
        $div.css('display', 'none');
        $btn.text("❌");
    }
    else {
        $form.css('display', 'none');
        $div.css('display', 'flex');
        $btn.text("✏️");
    }
}

$(document).ready(function() {
    $('.edit').click(function() {
        showForm($(this));
    });
});