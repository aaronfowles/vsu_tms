$(document).ready( function() {
     $(".task-checkbox").on("click", function() {
         var id = $(this).parent().parent().attr("id");
         clickedComplete(id);
     })
});

// Register completed button clicked
function clickedComplete(id) {
    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });
    $.ajax({
        type:"POST",
        url:"/app/task_completed/",
        data: {'tasklistitem_id':id},
        success: function() {
            var id_string = "#" + id.toString();
            $(id_string).empty();
            // Look into bootstrap collapse functionality
            $(id_string).animate({height: 0, opacity:0},400);
        }
    });
};

// If incomplete clicked, present user with reason request

// Callback from reason for incomplete

// Send changes to database

// Request updates from database




