$( document ).ready(function() {

    $('#signupmodal').click(function() {
        $('#form-modal-body').load('/accounts/register/', function () {
            $('#form-modal').modal('toggle');
            AjaxifyForm('#form-modal-body form', '#form-modal', '/analyze/');
        });
    });

});
