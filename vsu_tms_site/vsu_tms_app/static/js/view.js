$("#status").addClass(status_class);
$(document).ready( function() {
     $(".task-checkbox").on("click", function() {
         var id = $(this).parent().parent().attr("id");
         if ($(this).attr("id") == 'not-completed') {
             clickedNotComplete(id);
         } else if($(this).attr("id") == 'pending') {
             clickedPending(id);
         } else if($(this).attr("id") == 'complete') {
             clickedComplete(id);
         }
     });
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
	    $("#feedback").removeClass("alert-warning");
            $("#feedback").removeClass("alert-danger");
	    $("#feedback").addClass("alert-success");
            $("#feedback").text("Task Completed");
        }
    });
};

function clickedNotComplete(id) {
    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });
    $.ajax({
        type:"POST",
        url:"/app/task_not_completed/",
        data: {'tasklistitem_id':id},
        success: function() {
            var id_string = "#" + id.toString();
            $(id_string).empty();
	    $("#feedback").removeClass("alert-warning");
	    $("#feedback").removeClass("alert-success");
	    $("#feedback").addClass("alert-danger");
            $("#feedback").text("Task Not Completed");
        }
    });

};

function clickedPending(id) {
    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });
    $.ajax({
        type:"POST",
        url:"/app/task_pending/",
        data: {'tasklistitem_id':id},
        success: function() {
            var id_string = "#" + id.toString();
	    $(id_string).addClass("warning");
	    $(id_string).removeClass("danger");
	    $("#feedback").removeClass("alert-success");
	    $("#feedback").removeClass("alert-danger");
            $("#feedback").addClass("alert-warning");
            $("#feedback").text("Task In Progress");
        }
    });

};

// If incomplete clicked, present user with reason request

// Callback from reason for incomplete

// Send changes to database

// Request updates from database

// Function to hide hourly tasks which aren't due yet


