PERCENT_BAR_WIDTH = '50px';


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


function update_nav_items() {
    if( $('#user_id').val() == 'None' ) {
        // Always show
        $('#nav_support').show();

        $('#nav_login').show();

        $('#nav_logout').hide();
        $('#nav_my_recipes').hide();
        $('#nav_new_recipe').hide();
    } else {
        $('#nav_support').show();

        $('#nav_login').hide();

        $('#nav_logout').show();
        $('#nav_my_recipes').show();
        $('#nav_new_recipe').show();
    }
}

function get_recipe_form_data() {
    var data = {
//        recipe_id: $('#recipe_id').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    };
    data['name'] = $('#id_name').val();
    data['serves'] = $('#id_serves').val();
    data['private'] = $('#id_private').prop('checked');
    data['steps'] = $('#id_steps').val();

    var ingredients = [];
    $('#ingredients-list li').each(function () {
        ingredients.push({
            'sr17_id': $(this).attr('sr17'),
            'weight_id': $(this).attr('weight'),
            'unit': $(this).attr('unit'),
            'quantity': $(this).attr('quantity')
        });
    });
    data['ingredients'] = JSON.stringify(ingredients);
    return data;
}

function nutrition_table_updated_alert() {
    var $n = $('div.nutrition');
    var time_highlight_msec = 500;
    $n.addClass('updated');
    setTimeout(function() {
        $n.removeClass('updated');
    }, time_highlight_msec);
}


function display_nutrition(data) {

    function render(nutr_name, nutr_data, targets, servings) {
        // If nutr_name is a key in nutr_data, render it nicely with its value, target percentage, etc.
        // If it's not, it must be a nutrition section header so return it with no modification

        if (!nutr_data.hasOwnProperty(nutr_name))
            return nutr_name;

        var v = nutr_data[nutr_name]['value'];
        var str_val = "N/A";
        var NA = true;
        if (v !== null) {
            v /= servings;
            v_precision = v.toFixed(1);
            str_val = String(v_precision);
            NA = false;
        }

        // Try to retrieve target value, and calculate percentage of target value
        str_perc_of_target = '';
        if (targets.hasOwnProperty(nutr_name)) {
            if (NA) {
                str_perc_of_target = '0%';  // If nutrient value is not available, assume it's zero
            } else {
                target = targets[nutr_name];
                perc_of_target = 100.0 * v / target;
                str_perc_of_target = String(perc_of_target.toFixed(0)) + '%'
            }
        }

        var name = nutr_data[nutr_name]['name'].replace('Vitamin ', '');
        if (str_perc_of_target == '') {
            percent_bar_output = '<div class="progress-blank" style="float:right; display:inline-block; height:1px; width:' + PERCENT_BAR_WIDTH + ';"></div>';
        } else {
            percent_bar_output = '<div class="progress" style="width: ' + PERCENT_BAR_WIDTH +
            ';"><div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100" style="display:inline-block; width:' +
            str_perc_of_target +
            '" ><span>' + str_perc_of_target + '</span></div></div>';
        }
        if (str_val != "N/A") {
            str_val = str_val + ' ' + nutr_data[nutr_name]['unit'];
        }
        return '<span class="nutrient-name">' + name + '</span> ' +
            percent_bar_output +
            '<span class="nutrient-value">' + str_val + '</span>';
    }

    function create_nested_list(layout_list, target_div, render_fn, nutr_data, targets, servings) {
        for (var i=0; i < layout_list.length; i++) {

            // This element of the array is either a nutrient name, or another array
            if (layout_list[i] instanceof Array) {

                // Layout array element is a sub-array, so add a nested list
                var tmp = $('<ul></ul>').appendTo(target_div);
                create_nested_list(layout_list[i], tmp, render_fn, nutr_data, targets, servings);

            } else {

                // Layout array element is the name of a nutrient, so render it
                var nutr_name = layout_list[i];
                var html = render(nutr_name, nutr_data, targets, servings);

                // Try to retrieve target value, to be displayed on mouse-over only
                var tar = targets[nutr_name];
                if (targets.hasOwnProperty(nutr_name)) {
                    html = '<li title="target = ' + String(tar.toFixed(1)) + ' ' + nutr_data[nutr_name]['unit'] + '">' + html  + '</li>';
                } else {
                    html = '<li>' + html + '</li>';
                }
                var tmp = $(html).appendTo(target_div);
                $('<div style="clear:both;"></div>').appendTo(target_div);
            }
        }
    }

    var servings = $('#id_serves').val();
    if (isNaN(servings)) {
        alerts('Please specify how many servings this recipe makes.  The nutrition values are calculated for one serving.');
    }

    // Slicing is for column breaks
    $('#nutrition1').empty();
    create_nested_list(data['layout'].slice(0,7), $('#nutrition1'), render, data['nutr_data'], data['targets'], servings);
    $('#nutrition2').empty();
    create_nested_list(data['layout'].slice(7), $('#nutrition2'), render, data['nutr_data'], data['targets'], servings);
    nutrition_table_updated_alert();
}


function calculate_nutrition(ingredient_solo_pk) {

    // Any operation that requires an update to the nutrition table should remove solo mode, unless it's the solo mode button being pushed
    if (isNaN(ingredient_solo_pk)) remove_solo_styling();

    var servings = parseFloat($('#id_serves').val());
    if (isNaN(servings)) {
        alert('Please set the number of servings (Serves), so the nutrition values can be calculated.');
        return;
    }

    var ingredient_list = [];
    $('#ingredients-list li').each(function () {
        if (isNaN(ingredient_solo_pk) || ingredient_solo_pk == $(this).attr('sr17')) {
            ingredient_list.push({
                'sr17': $(this).attr('sr17'),
                'weight': $(this).attr('weight'),
                'unit': $(this).attr('unit'),
                'quantity': $(this).attr('quantity')
            });
        }
    });
    var send_data = {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        ingredients_list: JSON.stringify(ingredient_list)
    };

    $.ajax({
        traditional: true,  // avoid adding a character to 'ingredients' key in POST data (jQuery caters to PHP!)
        type: "POST",
        url: "/analyze/nutrition/",
        data: send_data,
        success: function (data) {
            $('#analyze_spinner').hide();
            display_nutrition(data);
        },
        error: function (jqXHR, textStatus, errorThrowndata) {
            $('#analyze_spinner').hide();
            console.log(jqXHR.responseText);
            alert("Sorry, we encountered an error while trying to retrieve nutritional data.")
        }
    });
    $('#analyze_spinner').show();
}


function remove_solo_styling() {
    var lis = $('#ingredients-list li');
    lis.removeClass('mute');
    lis.removeClass('solo');
}


function add_delete_buttons() {
    $(".delete-btn").remove();
    $('#ingredients-list li').each(function() {
        var x = $('<button type="button" class="btn btn-danger btn-xs pull-right delete-btn" title="delete this ingredient"><span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span> delete</button>');
        $(this).append(x);
        x.click(function () {
            $(this).parent().remove();
            calculate_nutrition();
        });
    });
}


function remove_delete_buttons() {
    $(".delete-btn").remove();
}


function remove_solo_buttons() {
    $(".solo-btn").remove();
    remove_solo_styling();
}


function add_solo_buttons() {
    $(".solo-btn").remove();
    $('#ingredients-list li').each(function() {
        var pk = $(this).attr('sr17');
        var b = $('<button type="button" class="btn btn-primary btn-xs pull-right solo-btn" title="show nutritional values for this ingredient only"><span class="glyphicon glyphicon-play-circle" aria-hidden="true"></span> solo</button>');
        $(this).append(b);
        b.click(function () {
            if ($(this).parent().hasClass('solo')) {
                remove_solo_styling();
                calculate_nutrition();
            } else {
                $(this).parent().parent().find('li').removeClass('solo');
                $(this).parent().parent().find('li').addClass('mute');
                $(this).parent().removeClass('mute');
                $(this).parent().addClass('solo');
                calculate_nutrition(pk);
            }
        });
    });
}


function add_ingredient_to_list(sr17, weight_pk, unit, quantity, description) {
    quantity_str = str_decimal_to_fraction(String(quantity));
    str = '<li sr17="' + String(sr17) + '" weight="' + weight_pk + '" unit="' + unit + '" quantity="' + quantity + '" class=clearfix ingr>' + quantity_str + ' ' + unit + ' ' + description + '</li>';
    $('ul#ingredients-list').append(str);
    add_solo_buttons();
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
    var r = data['recipe'];
    if (r['private'] == 'False') {
        r['private'] = false;
    } else {
        r['private'] = true;
    }
    $('#id_name').val(r['name']);
    $('#id_serves').val(r['serves']);
    $('#id_private').prop('checked', r['private']);
    $('#id_steps').val(r['steps']);
    $('#recipe_id').val(r['pk']);

    var str = '';
    var ingr = null;
    $('ul#ingredients-list').empty();
    for (var i=0; i < data.ingredients.length; i++) {
        ingr = data.ingredients[i];
        add_ingredient_to_list(ingr.sr17, ingr.weight, ingr.unit, ingr.quantity, ingr.description);
//        str = '<li sr17="' + String(ingr.sr17) + '" weight="' + ingr.weight + '" unit="' + ingr.unit + '" quantity="' + ingr.quantity + '" class=clearfix ingr>' + ingr.quantity + ' ' + ingr.unit + ' ' + ingr.description + '</li>';
//        $('ul#ingredients-list').append(str);
    }
    add_solo_buttons();

    if ($('#id_name').val())
        document.title = $('#id_name').val() + ' - recipelab';
    // Update URL (HTML5 only...)
    window.history.pushState(null, r['name'], '/analyze/'+ String(r['pk']) +'/');
}



function search_result_selected(event, ui) {
    event.preventDefault();  // By default, the "value" gets placed in the control, we want the label!
    $("#search").val(ui.item.label);
    $("#ingredient_pk").val(ui.item.value);

    $.ajax({
        type: 'GET',
        url: '/analyze/units/' + ui.item.value + '/',
        success: function (data) {
            // Load unit options
            $('#unit').empty();
            for (var k in data) {
                $('#unit').append('<option value="' + escapeHtml(k) + '">' + escapeHtml(data[k])+ '</option>');
            }
            $('#ingredient_spinner').hide();
            $('#unit').focus();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#ingredient_spinner').hide();
            alert("Sorry, we encountered an error while trying to retrieve the units of measure.")
            console.log(jqXHR.responseText);
        }
    });
    $('#ingredient_spinner').show();
}


function initialize_ingredient_popup() {
    $('#ingredient_spinner').hide();
    $('#search').val("");
    $('#unit').val("");
    $('#quantity').val("");
    $('#quantity').prop('type', 'number');

    $('#ingredient-form .form-group').removeClass('has-error');
    $('#ingredient-form .error-msg').remove();
}

// Open ingredient popup
function add_ingredient() {
    initialize_ingredient_popup();
    $('#ingredientModal').modal();
    $('#search').focus();
}


function fraction_to_decimal(f) {
    switch(f) {
        case '½':
            return '0.5';
        case '⅓':
            return '0.3333';
        case '¼':
            return '0.25';
        case '⅕':
            return '0.2';
        case '⅙':
            return '0.1667';
        case '⅛':
            return '0.125';
        case '⅔':
            return '0.6667';
        case '¾':
            return '0.75';
    }
    return f;
}

function str_decimal_to_fraction(d) {
    function close(n1, n2) {
        return (Math.abs(n1-n2) <= 0.001);
    }
    if (close(d, 0.5)) return '½';
    if (close(d, 0.3333)) return '⅓';
    if (close(d, 0.25)) return '¼';
    if (close(d, 0.2)) return '⅕';
    if (close(d, 0.1667)) return '⅙';
    if (close(d, 0.6667)) return '⅔';
    if (close(d, 0.75)) return '¾';
    return d;
}

function accept_ingredient() {
    // Clear previous error styling before doing validation
    $('#ingredient-form .form-group').removeClass('has-error');
    $('#ingredient-form .error-msg').remove();

    if ($('#ingredient_pk').val() == "") {
        $('#search').parents('.form-group').addClass('has-error');
        $('label[for=search]').append('<span class="error-msg"> : Please enter some search terms, then select a database matching ingredient from the drop-down list</span>');
        return;
    }

    var q = parseFloat(fraction_to_decimal($('#quantity').val()));
    if(isNaN(q)) {
        $('#quantity').parents('.form-group').addClass('has-error');
        $('label[for=quantity]').append('<span class="error-msg"> : Please enter a number</span>');
        return;
    }
    if ($('#unit').val() == "" || $('#unit').val() === null) {
        $('#unit').parents('.form-group').addClass('has-error');
        $('label[for=unit]').append('<span class="error-msg"> : Please select a unit of measure</span>');
        return;
    }
    add_ingredient_to_list($('#ingredient_pk').val(), $('#unit').val(), $('select#unit option:selected').text(), q, $("#search").val());
    initialize_ingredient_popup();
    calculate_nutrition();
}


function update_target_category() {
    $.ajax({
        type: 'get',
        url: "/analyze/get_target_category/",
        data: {},
        success: function (data) {
            $('#target_category_type').html(data.text); // Text on main page
            $('#target_category').val(data.category);
            $('#target_age').val(data.age);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText);
            alert("Sorry, we encountered an error while trying to retrieve target categories.")

        }
    });
}


function limit_target_age() {
    var age = $('#target_age').val();
    switch($('#target_category').val()) {
        case 'Males':
            if (age < 1) $('#target_age').val(1);
            if (age > 150) $('#target_age').val(150);
            break;
        case 'Females':
            if (age < 1) $('#target_age').val(1);
            if (age > 150) $('#target_age').val(150);
            break;
        case 'Pregnancy':
            if (age < 14) $('#target_age').val(14);
            if (age > 50) $('#target_age').val(50);
            break;
        case 'Lactation':
            if (age < 14) $('#target_age').val(14);
            if (age > 50) $('#target_age').val(50);
            break;
    }
}


function set_target() {
    $.ajax({
        type: 'post',
        url: "/analyze/set_target_category/",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            category: $('#target_category').val(),
            age: $('#target_age').val()
        },
        success: function (data) {
            update_target_category();
            calculate_nutrition();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText);
            alert("Sorry, we encountered an error while trying to set the target.")
        }
    });
}



$( document ).ready(function() {
    $('#calculate_spinner').hide();
    $('#save_spinner').hide();
    $('textarea').autosize();

    // Ingredient Edit / Done buttons
    $('#done').hide();
    $('#edit_delete').show();
    $("#edit_delete").click(function () {
        if ( $('#ingredients-list li').length > 0 ) {
            add_delete_buttons();
            remove_solo_buttons();
            $(this).hide();
            $('#done').show();
        }
    });
    $("#done").click(function () {
        remove_delete_buttons();
        add_solo_buttons();
        $(this).hide();
        $('#edit_delete').show();
    });


    $('#targets').click(function () {
        $('#targetModal').modal();
        update_target_category();
    });

    $('#set_target').click(function () {
        if($('#user_id').val() == 'None') {
            alert('To change the targets, please sign up for a free account.');
            return;
        }
        set_target();
    });
    $('#target_age').change(limit_target_age);
    $('#target_category').change(limit_target_age);


    $('#add_ingredient').click(function () {
        remove_delete_buttons();
        add_solo_buttons();
        $('#done').hide();
        $('#edit_delete').show();
        add_ingredient();
    });

    $('#accept_ingredient').click(accept_ingredient);

    // Ingredient popup search function
    $("#search").autocomplete( { source: "/analyze/search_ingredient/" });
    $("#search" ).autocomplete( "option", "appendTo", "#ingredientModal" );  // So the result list doesn't appear behind modal dialog
    $("#search").on("autocompleteselect", search_result_selected);
    $("#search").on("autocompletesearch", function( event, ui ) {
        $('#ingredient_spinner').show(); $('#ingredient_pk').val("");
        $('#ingredient-form .form-group').removeClass('has-error');
        $('#ingredient-form .error-msg').remove();
    } );  // Whenever the user types in something new, empty out the ingredient ID we've hidden
    $("#search").on("autocompleteresponse", function( event, ui ) {
        $('#ingredient_spinner').hide();
        if (ui.content.length == 0) {
            $('#search').parents('.form-group').addClass('has-error');
            $('label[for=search]').append('<span class="error-msg"> : Not found</span>');
        }
    } );

    var frm = $('#recipe-form');
    frm.submit(function (ev) {
        if($('#user_id').val() == 'None') {
            alert('To save a recipe, please sign up for a free account.');
            return;
        }
        var url = '/analyze/save_recipe/';
        if ($('#recipe_id').val() != 'None') {
            url = url + $('#recipe_id').val() + '/';
        }
        $.ajax({
            traditional: true,  // avoid adding a character to 'ingredients' key in POST data (jQuery caters to PHP!)
            type: frm.attr('method'),
            url: url,
            data: get_recipe_form_data(),
            success: function (data) {
                $('#save_spinner').hide();

                // No django Form errors
                if (!data.hasOwnProperty('errors')) {
                    $('#recipe_id').val(data['pk']);
                    // HTML5 only!
                    window.history.pushState(null, $('#id_name').val(), '/analyze/'+ String($('#recipe_id').val()) +'/');
                    if ($('#id_name').val())
                        document.title = $('#id_name').val() + ' - recipelab';
                }

            },
            error: function (jqXHR, textStatus, errorThrowndata) {
                $('#save_spinner').hide();
                console.log(jqXHR.responseText);
                alert("Sorry, we encountered an error while trying to save the recipe.")
            }
         });
        ev.preventDefault();
        $('#id_name').focus(); // Move focus away from button so Bootstrap changes its colour back
        $('#save_spinner').show();
    });

    // Retrieve recipe data (unless this is a blank form)
    if ($('#recipe_id').val() != 'None') {
        var frm = $('#recipe-form');
        $.ajax({
            type: 'get',
            url: "/analyze/recipe/" + $('#recipe_id').val() + "/",
            data: {},
            success: function (data) {
                put_recipe_form_data(data);
                // Update global-scope nutrition data
                nutrition_data = data['nutrition_data'];
                nutrition_layout = data['nutrition_layout'];
                target_data = data['target_data'];
                calculate_nutrition();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.responseText);
                alert("Sorry, we encountered an error while trying to retrieve this recipe.")
            }
        });
    } else {
        $('#id_serves').val(1);    // Set default servings here, since the server sends only a template when you ask for a blank recipe (no django form with default Model values)
        calculate_nutrition();
    }

    $('#id_serves').on('input propertychange paste', function () {
        if ($('#id_serves').val()) {
            calculate_nutrition();
        }
    });


    function capture_user_id(xhr) {
        // Instantiate a jQuery object using the returned HTML
        var obj = $('<div/>').html(xhr).contents();

        // Copy newly-returned User ID and CSRF token to hidden form fields to sastify page logic and also django (when we next try to save a recipe)
        var id = obj.find('#user_id').val();
        $('#user_id').val(id);
        var csrf = obj.find('#csrf_update').val();
        $('input[name=csrfmiddlewaretoken]').val(csrf);

        // Cosmetic adjustments for user new logged in
        $('signupmodal').hide();
        update_nav_items();
    }
    $('#signupmodal').click(function() {
        $('#form-modal-body').load('/accounts/register/', function () {
            $('#form-modal').modal('toggle');
            AjaxifyForm('#form-modal-body form', '#form-modal',capture_user_id);
        });
    });

    $('.fraction').click(function() {
        var str = $(this).attr('valstr');
        var num = $(this).attr('valnum');
        $('#quantity').prop('type', 'text');  // The quantity box is usually type="number", which will not accept these fraction strings
        $('#quantity').val(str);
    });


    update_target_category();
    update_nav_items();
});



