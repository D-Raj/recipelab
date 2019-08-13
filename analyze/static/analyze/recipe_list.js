
function delete_recipe(pk) {
    $.ajax({
        type: 'get',
        url: "/analyze/delete_recipe/" + pk + "/",
        data: {},
        success: function (data) {
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText);
            alert("Sorry, we encountered an error while trying to delete this recipe.")
        }
    });
}

function add_delete_buttons() {
    $(".delete-btn").remove();
    $('#recipes li').each(function() {
        var x = $('<button type="button" class="btn btn-danger btn-xs delete-btn" title="delete this recipe"><span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span> delete</button> ');
        $(this).prepend(x);
        x.click(function () {
            delete_recipe($(this).parent().attr('pk'));
            $(this).parent().remove();
        });
    });
}


function remove_delete_buttons() {
    $(".delete-btn").remove();
}


$( document ).ready(function() {

    // Ingredient Edit / Done buttons
    $('#done').hide();
    $('#edit_delete').show();
    $("#edit_delete").click(function () {
        if ( $('#recipes li').length > 0 ) {
            add_delete_buttons();
            $(this).hide();
            $('#done').show();
        }
    });
    $("#done").click(function () {
        remove_delete_buttons();
        $(this).hide();
        $('#edit_delete').show();
    });

});
