
    /* Borrowed from https://dmorgan.info/posts/django-views-bootstrap-modals
     * Convert a normal django form into an AJAX form. Works great for modal forms
     *
     *     Submit via AJAX call
     *     Show errors if any
     *     Close modal box and redirect (or not)
     *
     * Invoke this function as you open/load the modal form, as follows:
     *     $('#comment-button').click(function() {
     *         $('#form-modal-body').load('/test-form/', function () {
     *             $('#form-modal').modal('toggle');
     *             AjaxifyForm('#form-modal-body form', '#form-modal', 'http://blah/redirect.html');
     *         });
     *     });
     */
    var AjaxifyForm = function(form, modal, redirect) {
        $(form).submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (xhr, ajaxOptions, thrownError) {
                    if ( $(xhr).find('.has-error').length > 0 ) {
                        $(modal).find('.modal-body').html(xhr);
                        AjaxifyForm(form, modal, redirect);
                    } else {
                        $(modal).modal('toggle');
                        if ($.isFunction(redirect)) {
                            redirect(xhr);                // User supplied a callable to handle successful form submission
                        }
                        else if (! (redirect === undefined) ) {
                            window.location.replace(redirect);
                        }
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    // handle response errors here
                }
            });
        });
    };

