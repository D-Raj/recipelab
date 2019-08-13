MIN_RECIPE_LINES = 7;
fields = [ 'name', 'serves', 'private', 'steps' ];  // ingredient box is treated separately

var nutrition_data = [];
var target_data = [];
var nutrition_layout = [];
var prev_num_ingredient_lines = 0;


// ---------------------------------------
var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };
function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
      return entityMap[s];
    });
}
// ---------------------------------------


function nutrition_table_updated_alert() {
    var $n = $('div.nutrition');
    var time_highlight_msec = 500;
    $n.addClass('updated');
    setTimeout(function() {
        $n.removeClass('updated');
    }, time_highlight_msec);
}

function percent_bars_update() {
    $('div.percent-bar').each(function () {
        var txt = $(this).html();
        if (txt != "") {
            $(this).parent().show();
            $(this).css('width', txt);
        } else {
            $(this).parent().hide();
        }
    });

}

function display_nutrition(ingredient_solo_pk) {
    if (ingredient_solo_pk === null) {
        remove_solo_styling();
    }
    var servings = parseFloat($('#id_serves').val());
    var data = nutrition_data;  // An object with ingredient PK's as its attributes.  Each attribute's value is an object with db_field nutrition names as its attributes
    var targets = target_data;
    if (isNaN(servings)) {
        alert('Please set the number of servings (Serves), so the nutrition values can be calculated.');
        return;
    }
    function render(nutr_name) {
        // If nutr_name makes the name an ingredient's attributes, render it nicely with its value, target percentage, etc.
        // If it's not an ingredient attribute name, it must be a nutrition section header so return it with no modification

        // Get list of nutritient names (take first ingredient in data set. the variable data is in scope of enclosing function)
        if (Object.keys(data).length > 0) {  // TODO: Not compatible with IE8 and earlier
            var first_ingredient = data[Object.keys(data)[0]];
            var nutrients = Object.keys(first_ingredient);

            if ($.inArray(nutr_name, nutrients) != -1) {
                var v = 0.0;
                var NA = true;
                for (var ingr in data) {
                    // Solo mode
                    if (ingredient_solo_pk !== null && ingr != ingredient_solo_pk) {
                        continue;
                    }
                    if (data[ingr][nutr_name].value !== null) {
                        v += data[ingr][nutr_name].value;
                        NA = false;
                    }
                }
                var str_val;
                var str_perc_of_target = '';
                if (NA) {
                    str_val = 'N/A';
                } else {
                    v /= servings;
                    v_precision = v.toFixed(1);
                    str_val = String(v_precision);
                }

                // Try to retrieve target value, and calculate percentage of target value
//                    if ($.inArray(nutr_name, targets) != -1) {
                if (targets.hasOwnProperty(nutr_name)) {
                    if (NA) {
                        str_perc_of_target = '0%';  // If nutrient value is not available, assume it's zero
                    } else {
                        target = targets[nutr_name];
                        perc_of_target = 100.0 * v / target;
                        str_perc_of_target = String(perc_of_target.toFixed(0)) + '%'
                    }
                }

                var name = first_ingredient[nutr_name].name.replace('Vitamin ', '');
                var bar_width = '30px'
                if (str_perc_of_target == '') {
                    percent_bar_output = '<div class="progress-blank" style="float:right; display:inline-block; height:1px; width:' + bar_width + ';"></div>'
                } else {
                    percent_bar_output = '<div class="progress" style="width: 30px;"><div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100" style="display:inline-block; width:' +
                        str_perc_of_target +
                        '" ><span>'+ str_perc_of_target +'</span></div></div>';
                }
                if (str_val != "N/A") {
                    str_val = str_val + ' ' + first_ingredient[nutr_name].unit;
                }
                output = '<span class="nutrient-name">' + name + '</span> ' +
                    percent_bar_output +
                    '<span class="nutrient-value">' + str_val + '</span>';

//                    '<div class="nutrient-percent"><div class="percent-border"><div class="percent-bar">' + str_perc_of_target + '</div></div></div>' +

                return output
            }
            return nutr_name;
        }
        return nutr_name;
    }
    function create_nested_list(list, element, render) {
        for (var i=0; i < list.length; i++) {
            if (list[i] instanceof Array) {
                var tmp = $('<ul></ul>').appendTo(element);
                create_nested_list(list[i], tmp, render);
            } else {
                var tmp = $('<li>' + render(list[i]) + '</li>').appendTo(element);
                $('<div style="clear:both;"></div>').appendTo(element);
            }
        }
    }

    // Slicing is for column breaks
    $('#nutrition1').empty();
    create_nested_list(nutrition_layout.slice(0,8), $('#nutrition1'), render);
    $('#nutrition2').empty();
    create_nested_list(nutrition_layout.slice(8), $('#nutrition2'), render);
    percent_bars_update();
    nutrition_table_updated_alert();
}


function get_recipe_form_data() {
    var data = {
        recipe_id: $('#recipe_id').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    };
    data['name'] = $('#id_name').val();
    data['serves'] = $('#id_serves').val();
    data['private'] = $('#id_private').prop('checked');
    data['steps'] = $('#id_steps').val();

    var ingredients = [];
    $('#ingredients-list li').each(function () {
        ingredients.push({
            'pk': $(this).attr('pk'),
            'text': text_no_solo($(this)),
        });
    });
    data['ingredients'] = JSON.stringify(ingredients);
    return data;
}

function text_no_solo($j) {
    var $k = $j.clone();
    $k.find('button').remove();
    return $k.text();
}

function ingredient_on_doubleclick() {
    var pk = $(this).attr('pk');
    var line_num = $('#ingredients-list li').index($(this));
    clear_ingredient_form();
    $('#ingredientModal').modal();

    $('#id_quantity').focus();  // Most move focus away from ingredients div so we can capture/prevent future focus on ingredients div
    $.ajax({
        traditional: true,
        type: 'POST',
        data: {
            open: true,
            pk: $(this).attr('pk'),
            desc: text_no_solo($(this)),
            recipe: $('#recipe_id').val(),
            line_num: line_num,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        url: '/analyze/ingredient/',
        success: function (data) {
            put_ingredient_form_data(data);
            $('#ingredient_spinner2').hide();
        },
        error: function (jqXHR, textStatus, errorThrowndata) {
            $('#ingredient_spinner2').hide();
            console.log(jqXHR.responseText);
        }
    });
    $('#ingredient_spinner2').show();
}

function remove_solo_styling() {
    var lis = $('#ingredients-list li');
    lis.removeClass('mute');
    lis.removeClass('solo');
}

function add_solo_buttons() {
    $('#ingredients-list li').each(function() {
        var pk = $(this).attr('pk');
        var b = $('<button type="button" class="btn btn-primary btn-xs pull-right solo-btn">solo</button>');
        $(this).append(b);
        b.click(function () {
            if ($(this).parent().hasClass('solo')) {
                display_nutrition(null);  // This will also remove solo styling
            } else {
                display_nutrition(pk);
                $(this).parent().parent().find('li').removeClass('solo');
                $(this).parent().parent().find('li').addClass('mute');
                $(this).parent().removeClass('mute');
                $(this).parent().addClass('solo');
            }
        });
    });
}

function remove_solo_buttons() {
    $('.solo-btn').remove();
    remove_solo_styling();
}

function put_recipe_form_data(data) {
    // Remove all error styling, then put it back as required
    $('.form-group').removeClass('has-error');
    $('.error-msg').remove();

    // Display errors
    if (data.hasOwnProperty('errors')) {
        for (var field in data.errors) {
            field_errors = data.errors[field];
            $('#id_'+field).parents('.form-group').addClass('has-error');
            $('label[for=id_'+ field+']').append('<span class="error-msg"> : ' + field_errors[0] + '</span>');
        }
        return;
    }

    // Display field values
    $('#id_name').val(data['name']);
    $('#id_serves').val(data['serves']);
    $('#id_private').prop('checked', data['private']);
    $('#id_steps').val(data['steps']);
    $('#recipe_id').val(data['pk']);

    // Refill ingredient <ul>
//    $('#to_improve').show();
    var l = $('#ingredients-list');
    l.empty();
    var i = 0;
    for (i=0; i<data['ingredients'].length; i++) {
        var ingr = data['ingredients'][i];
        if (ingr.user_verified == "True") {
            conf_class = 'confidence-high';
//        } else if (ingr.confidence_unit > 0.9 && ingr.confidence_food > 0.9) {
//            conf_class = 'confidence-medium';
        } else {
            conf_class = 'confidence-low';
        }
        var title = 'Matched: ' + String(ingr.quantity) + ' ' + ingr.unit + ' ' + ingr.sr17;
        // clearfix is for alignment of solo buttons
        l.append('<li pk="' + String(ingr.pk) + '" class="clearfix ingr ' + conf_class + '" title="' + title + '">' + ingr.description + '</li>');
//        l.append('<li pk="' + String(ingr.pk) + '" class="ingr ' + conf_class + '"><span title="'+  title + '">' + ingr.description + '</span></li>');

            // + ' confidence_food=' + String(ingr.confidence_food) + ' confidence_unit=' + String(ingr.confidence_unit)
            //        l.append('<li class="clearfix ' + ingr_class + '"><span title="'+  span_text + '">' + ingr.description + '</span><button type="button" class="btn btn-default btn-xs pull-right">details</button></li>');

    }

    // Reset ingredient state so we can detect further changes:
    $('#ingredients-list li').each(function () {
        $(this).attr('old_text', escapeHtml( $(this).text() ));
    });

    // Make ingredients double-clickable
    $('li.ingr').dblclick(ingredient_on_doubleclick);

    add_solo_buttons();

    nutrition_data = data['nutrition_data'];
    nutrition_layout = data['nutrition_layout'];
    target_data = data['target_data'];
    display_nutrition(null);

    // Add some blank lines at the bottom to keep the box open and pretty
    for (var j=0; j<(MIN_RECIPE_LINES-i); j++) {
        l.append('<li><br/></li>');
    }
    prev_num_ingredient_lines = $('#ingredients-list li').length;

    // Update URL (HTML5 only...)
    window.history.pushState(null, data['name'], '/analyze/'+ String(data['pk']) +'/');
}


function clear_ingredient_form() {
    $('div.ingredient .form-group').removeClass('has-error');
    $('div.ingredient .error-msg').remove();
    $('#id_sr17').empty();
    $('#id_unit').empty();
    $('#id_quantity').val('');
}


function put_ingredient_form_data(data) {
    // Remove all error styling, then put it back as required
    $('#match_improvement_request').show();
    $('#no_match_found').hide();
    $('#accept_button').show();
    $('#ingredient-form .form-group').removeClass('has-error');
    $('#ingredient-form .error-msg').remove();


    if (data.sr17 == 'None') {
        $('#match_improvement_request').hide();
        $('#no_match_found').show();
        $('#accept_button').hide();
    }

    // Display django form errors
    if (data.hasOwnProperty('errors')) {
        for (var field in data.errors) {
            field_errors = data.errors[field];
            // django Form-level errors are listed under __all__
            if (field == '__all__') {
                // dirty hack
                if (field_errors[0] == 'Please choose a unit.') {
                    $('#id_unit').parents('.form-group').addClass('has-error');
                    $('label[for=id_unit]').append('<span class="error-msg"> : ' + field_errors[0] + '</span>');
                }
            } else {
                field_errors = data.errors[field];
                $('#id_' + field).parents('.form-group').addClass('has-error');
                $('label[for=id_' + field + ']').append('<span class="error-msg"> : ' + field_errors[0] + '</span>');
            }
        }
        return;
    }

    // Load unit options
    $('#id_unit').empty();
    for (var i=0; i < data['units'].length; i++) {
        $('#id_unit').append('<option value="' + escapeHtml(data['units'][i]) + '">' + data['units'][i]+ '</option>');
    }

    // Load food match options
    $('#id_sr17').empty();
    for (var i=0; i < data['foods'].length; i++) {
        $('#id_sr17').append('<option value="' + String(data['foods'][i].pk) + '">' + data['foods'][i].desc + '</option>');
    }

    // Display field values
    $('#id_quantity').val(data['quantity']);
    $('#id_unit').val(data['unit']);
    $('#id_sr17 option:eq(0)').prop('selected', true); // First food in dropdown box is always the current one used
    $('#id_unit option:eq(0)').prop('selected', true); // First unit in dropdown box is always the current one used
    $('#ingredient_id').val(data['pk']);

    // Refresh nutrition table on main recipe form
    if (data.hasOwnProperty('nutrition_data')) {
        nutrition_data = data['nutrition_data'];
        nutrition_layout = data['nutrition_layout'];
        target_data = data['target_data'];
        display_nutrition(null);
    }

    // Update PK of ingredient on the recipe form, in case this is a newly created one
    // This relies on the line_number being correct, which is only true if it's a new ingredient or one with a newly changed description
    // Don't bother if there's already an ingredient with this pk (as an attribute)
    if ($("#ingredients-list li[pk='" + data['pk'] + "']").length == 0) {
        $("#ingredients-list li").eq(data['line_number']).attr('pk', data['pk']);
    }

    // Update confidence class of ingredient <li> on the recipe form - this will pinken anything unverified
    $("#ingredients-list li[pk='" + data['pk'] + "']").each(function () {
        $(this).removeClass('confidence-high');
        $(this).removeClass('confidence-medium');
        $(this).removeClass('confidence-low');
        if (data['user_verified'] == 'True') {
            $(this).addClass('confidence-high');
        } else {
            $(this).addClass('confidence-low');
        }
    });

}

function get_ingredient_form_data() {
    // Remove all error styling, then put it back as required
    $('div.ingredient .form-group').removeClass('has-error');
    $('div.ingredient .error-msg').remove();

    var data = {
        pk: $('#ingredient_id').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        unit: $('#id_unit').val(),
        sr17: $('#id_sr17').val(),
        quantity: $('#id_quantity').val()
    };
    return data;
}


// =============================================================================================================

$( document ).ready(function() {
    $('#analyze_spinner').hide();
    $('#ingredient_spinner').hide();
    $('#ingredient_spinner2').hide();
    $('textarea').autosize();
//    $('#to_improve').hide();

    $('#targets').click(function () {
        $('#targetModal').modal();
    });

    $('#id_sr17').change(function () {
        $.ajax({
            type: 'GET',
            data: $('#id_sr17').val(),
            url: '/analyze/units/' + String($('#id_sr17').val()) + '/',
            success: function (data) {
                // Load unit options
                var prev_unit = $('#id_unit').val();
                $('#id_unit').empty();
                for (var i=0; i < data['units'].length; i++) {
                    $('#id_unit').append('<option value="' + escapeHtml(data['units'][i]) + '">' + data['units'][i]+ '</option>');
                }
                if ($.inArray(prev_unit, data['units']) != -1) {
                    $('#id_unit').val(prev_unit);
                }
                $('#ingredient_spinner').hide();
                $('#id_unit').focus();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#ingredient_spinner').hide();
                console.log(jqXHR.responseText);
            }
        });
        $('#ingredient_spinner').show();
    });

    $('#ingredient-form').submit(function (ev) {
        $.ajax({
            traditional: true,  // avoid adding a character to 'ingredients' key in POST data (jQuery caters to PHP!)
            type: 'POST',
            url: '/analyze/ingredient/',
            data: get_ingredient_form_data(),
            success: function (data) {
                put_ingredient_form_data(data);
                $('#ingredient_spinner').hide();
                if (!data.hasOwnProperty('errors')) {
                    $('#ingredientModal').modal('hide');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#ingredient_spinner').hide();
                console.log(jqXHR.responseText);
            }
        });
        ev.preventDefault();
        $('#id_name').focus(); // Move focus away from button so Bootstrap changes its colour back
        $('#ingredient_spinner').show();
    });


    var frm = $('#recipe-form');
    frm.submit(function (ev) {
        $.ajax({
            traditional: true,  // avoid adding a character to 'ingredients' key in POST data (jQuery caters to PHP!)
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: get_recipe_form_data(),
            success: function (data) {
                put_recipe_form_data(data);
                $('#analyze_spinner').hide();
            },
            error: function (jqXHR, textStatus, errorThrowndata) {
                $('#analyze_spinner').hide();
                console.log(jqXHR.responseText);
            }
         });
        ev.preventDefault();
        $('#id_name').focus(); // Move focus away from button so Bootstrap changes its colour back
        $('#analyze_spinner').show();
    });


    // Run this once on the container holding the contentEditable components
    // Using jQuery plugin:
    //     https://github.com/makesites/jquery-contenteditable
    $("div.ingredients").contentEditable().change(function(e){
        var changed = false;

        // Don't let the box collapse to nothingness (if you keep hitting delete/backspace, you can
        // even wipe out the last <li>
        var num_ingredient_lines = $('#ingredients-list li').length;
        for (var j=0; j<(MIN_RECIPE_LINES-num_ingredient_lines); j++) {
            $('#ingredients-list').append('<li><br/></li>');
        }

        // If you create a new <li> in the ingredient box by hitting enter at the end of
        // an existing <li>, the new one will inherit the existing <li>'s attributes and classes. Prevent this!
        // Should only get a confidence class.
        // This is true also of any <li> where the user has deleted all the characters (now empty), in that
        // case it's also important to remove the double-click event handler.
        $('#ingredients-list li').each(function () {
            if (text_no_solo($(this)) == '') {
                $(this).removeClass('confidence-high');
                $(this).removeClass('confidence-medium');
                $(this).removeClass('confidence-low');
                $(this).removeAttr('title');
                $(this).removeAttr('pk');
                $(this).removeAttr('old_text');
                $(this).unbind();
            }
        });

        // Detect creation of a new ingredient - any non-blank <li> that doesn't have a confidence class yet
        $('#ingredients-list li').each(function () {
            if (text_no_solo($(this)) != '' &&
                !($(this).hasClass('confidence-high') || $(this).hasClass('confidence-medium') || $(this).hasClass('confidence-low'))) {
                // Make new ingredient double-clickable
                $(this).dblclick(ingredient_on_doubleclick);
                // Set confidence to low
                $(this).addClass('confidence-low');
                changed = true;
            }
        });

        // Reset confidence class for any pk which has been edited
        $('#ingredients-list li').each(function () {
            if ($(this).attr('old_text') !== undefined && escapeHtml( text_no_solo($(this)) ) != $(this).attr('old_text')) {
                $(this).removeClass('confidence-high');
                $(this).removeClass('confidence-medium');
                $(this).removeClass('confidence-low');
                $(this).addClass('confidence-low');
                changed = true;
            }


        });

        // Occurs if user removes/adds an <li>
        if (prev_num_ingredient_lines != num_ingredient_lines) {
            changed = true;
        }

        if (changed) {
            remove_solo_buttons();
        }

        // Refresh ingredient state so we can detect further changes
        $(this).attr('old_text', escapeHtml( text_no_solo($(this)) ));
        prev_num_ingredient_lines = num_ingredient_lines;

//        console.log(e);
//        $(".output .action").html(e.action);
//        for(i in e.changed){
//            $(".output .key").html(i);
//        }
    });

    $('[contenteditable]').focus(function() {
    });

    // If user copies text from another web page, must avoid pasting the HTML tags.
    // Best solution:
    //     http://stackoverflow.com/questions/12027137/javascript-trick-for-paste-as-plain-text-in-execcommand
    // Other solutions:
    //     https://github.com/samshelley/contentEditable  (browser compatibility issues)
    //     http://stackoverflow.com/questions/15125217/convert-html-to-plain-text-in-contenteditable  (complicated, tries to keep track of caret position)
    //     http://jsfiddle.net/erikwoods/Ee3yC/  (clunky, requires user to paste into a modal popup box)
    //
    $('[contenteditable]').on('paste', function (e) {
        e.preventDefault();

        var text = '';
        var that = $(this);

        if (e.clipboardData)
            text = e.clipboardData.getData('text/plain');
        else if (window.clipboardData)
            text = window.clipboardData.getData('Text');
        else if (e.originalEvent.clipboardData)
            text = $('<div></div>').text(e.originalEvent.clipboardData.getData('text'));

        if (document.queryCommandSupported('insertText')) {
            // document.execCommand('insertHTML', false, $(text).html()); // strips newlines, not good for pasted recipe
            document.execCommand('insertText', false, $(text).html());
            return false;
        }
        else { // IE > 7
            that.find('*').each(function () {
                $(this).addClass('within');
            });

            setTimeout(function () {
                // nochmal alle durchlaufen
                that.find('*').each(function () {
                    // wenn das element keine klasse 'within' hat, dann unwrap
                    // http://api.jquery.com/unwrap/
                    $(this).not('.within').contents().unwrap();
                });
            }, 1);
        }
    });

    // PAGE LOAD TIME
    //
    // Make some space in the ingredient box
    var l = $('#ingredients-list');
    for (var j=0; j<MIN_RECIPE_LINES; j++) {
        l.append('<li><br/></li>');
    }
    // Retrieve recipe data (unless this is a blank form)
    if ($('#recipe_id').val() != 'None') {
        var frm = $('#recipe-form');
        $.ajax({
            type: 'get',
            url: frm.attr('action'),
            data: {},
            success: function (data) {
                put_recipe_form_data(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.responseText);
            }
        });
    } else {
        $('#id_serves').val(1);    // Set default servings here, since the server sends only a template when you ask for a blank recipe (no django form with default Model values)
    }

});
