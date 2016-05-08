$("#status").addClass(status_class);
var id_global = '';
$(document).ready( function() {
     $(".task-checkbox").on("click", function() {
         id_global = $(this).parent().parent().attr("id");
         if ($(this).attr("id") == 'not-completed') {
             $("#dialog").show();
         } else if($(this).attr("id") == 'pending') {
             clickedPending(id_global);
         } else if($(this).attr("id") == 'complete') {
             clickedComplete(id_global);
         }
     });
     $("#dialog").hide();
     $("#submit-not-clicked").on("click", function() {
          clickedNotComplete(id_global,document.getElementById('reason').value);
	  $("#dialog").hide();
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

function clickedNotComplete(id,reason) {
    $.ajaxSetup({
        beforeSend: function (xhr)
        {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });
    $.ajax({
        type:"POST",
        url:"/app/task_not_completed/",
        data: {'tasklistitem_id':id, 'reason':reason},
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

function sendNotComplete(id) {
    clickedNotComplete(id,reason);
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


