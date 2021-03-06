
$(function(){
    open_panel_if_needed();
    check_disabled_controls();

    // All of the actions to handle forms are tied to Click events on Apply
    // buttons. However, the browser will also try to submit forms if you hit
    // the Enter key, which bypasses the actions the Click event. This
    // instruction disables the Enter key inside forms.
    $(document).on('keypress', 'form.ajax', function(event){
        if (event.charCode == 13) {
        	event.preventDefault();
        }
    })

    $(document).on('click', 'form.ajax .btn-cancel, .btn-cancel[form]', function(){
        var form = $(this).closest('form');
        var attachment = $(this).attr('form');
        if(typeof attachment !== 'undefined')
            form = $('#' + attachment)
        var $container = form.closest('div');
        $("#unsaved-form-header").addClass("hidden");
        if($container.closest('.layout-panel').attr('id') == 'main-panel'){
            window.location.reload()
        }else{
            clear_form_populate_panel($container);
        }
    })

    $(document).on("click", '.btn-save', function () {
        $("#unsaved-form-header").addClass("hidden");
    })

    $(document).on('click', '#assign-function', function(){
        var $form = $(this).closest('.layout-panel').find('form')
        if($form.length){
            $form = $form.first()
            var action = $form.attr('action')
            var model = action.split('/')[2]
            var pk = action.split('/')[3] //the edit action URL has the pk in it
            var parent_select = get_parent_select($form)
            $(this).popover('destroy')
            if(parent_select != null){
                if(parent_select.attr('data-new-item-url').indexOf(model) != -1){ //correct model
                    if(pk != 'new'){
                        parent_select.val(pk)
                        parent_select.closest('.layout-panel').find('.btn-save').removeAttr('disabled'); //unsaved changes
                        parent_select.closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
                        document.getElementById("unsaved-form-header").classList.remove('hidden'); //unsaved changes
                    }
                }else{
                    $(this).popover({'content': "Cannot assign a probability function to a relational field, or vice versa",
                                     'trigger': 'focus'}) //placement bottom would be nice, but it gets cut off by the panel
                    $(this).popover('show')
                }
            }else{
                $(this).popover({'content': "No active fields to assign",
                                 'trigger': 'focus'})
                $(this).popover('show')
            }
        }
    })

    $('form[action^="/setup/RelationalFunction"]').livequery(function(){
        var action = $(this).attr('action');
        // The last part of the action URL is either "/new/" or a numeric ID of
        // an existing function to edit.
        if (action.indexOf('/new/', action.length-5) != -1) { // does action end with "new"?
            make_function_panel_editable(); //new forms should come in editable
        } else {
            // Existing functions should not be editable until the Edit button
            // is used.
            $('#functions_panel input').prop('disabled', true);
            $('#functions_panel select').prop('disabled', true);
            $('#functions_panel textarea').prop('disabled', true);
        };
        // activate the corresponding toolbar button
        document.getElementById('TB_functions').classList.add('active');
    })

    $('form[action^="/setup/ProbabilityDensityFunction"]').livequery(function(){
        var action = $(this).attr('action');
        // The last part of the action URL is either "/new/" or a numeric ID of
        // an existing function to edit.
        if (action.indexOf('/new/', action.length-5) != -1) {  // does action end with "new"?
            make_function_panel_editable(); //new forms should come in editable
        } else {
            // Existing functions should not be editable until the Edit button
            // is used.
            $('#functions_panel input').prop('disabled', true);
            $('#functions_panel select').prop('disabled', true);
            $('#functions_panel textarea').prop('disabled', true);
        };
        // activate the corresponding toolbar button
        document.getElementById('TB_functions').classList.add('active');
    })


    $(document).on('click', '#functions_panel span', function(event){
        $('.function_dropdown').removeClass('in');
    })

    //$(document).on('change', '#functions_panel input', function(event){
    //    var $form = $(this).closest('form')
    //    var load_target = $('#function-graph')
    //    var formAction = load_target.attr('src');
    //    var formData = new FormData($form[0])
    //    ajax_submit_complex_form_and_replaceWith(formAction, formData, $form, load_target);
    //})

    $(document).on('click', '.TB_btn', function(){
        var already_open = $(this).hasClass('active') //check before altering anything
        $('.TB_btn.active').removeClass('active') //close anything that might be open
        $('.TB_panel').addClass('TB_panel_closed')

        if(!already_open){
            $(this).addClass('active')
            var target_str = $(this).attr('TB-target')
            $(target_str).removeClass('TB_panel_closed')
        }
    })
    
    $(document).on('click', 'a[load-target]', function(event){
        event.preventDefault();
        load_target_link.call(this);
    });
    
    $(document).on('click', '[data-click-toggle]', function(){
        $(this).toggleClass($(this).attr('data-click-toggle'));
    });

    $(document).on('click', '#save_scenario', function(event){
        event.preventDefault();
        if($('.filename input').val() == 'Untitled Scenario'){
            prompt_for_new_file_name('/app/SaveScenario/');
        } else {
            $('#save_scenario').closest('form').submit() //normal submission
        }
    })

    $(document).on('submit', '.ajax', function(event) {
        event.preventDefault();
        var $self = $(this)
        var formAction = $(this).attr('action');
        var formData = new FormData($self[0])
        var load_target = $self
        var loading_message = $self.attr('data-loading-message') || "Working..."
        if($self.parent().hasClass('fragment')){
            load_target = $self.parent()
        }
        var success_callback = null;
        if(window.location.pathname.indexOf('setup/ControlProtocol/') != -1) {
            success_callback = function(){
                rebuild_protocols_list();
            }
        }
        if($self.parent().find('button[type=submit]').hasClass('btn-danger')) {// MOST IMPORTANT: for deleting outputs on form submission
            success_callback = function () {
                //window.location.reload()
                window.location.href = "/LoadingScreen/?loading_url=" + window.location.pathname;
            };  //updates Navigation bar context
        }
        ajax_submit_complex_form_and_replaceWith(formAction, formData, $self, load_target, loading_message, success_callback);
    });

    $(document).on('click', '#update_adsm', function(event){
        event.preventDefault();
        $.get('/app/Update/', function(result){ });
    });

    $(document).on('saved', 'form:has(.unsaved)', function(){ //fixes 'Save' button with wrong color state
        $(this).find('.unsaved').removeClass('unsaved');
    });

    $(document).on('click', '.open_scenario', function(event){ // #new_scenario is handled by [data-copy-link]
        var dialog = check_file_saved();
        if(dialog){
            event.preventDefault();
            var link = $(this).attr('href');
            dialog.$modal.on('hidden.bs.modal', function(){
                window.location = link})
        }
    });

    $(document).on('click', '[data-discard-changes-link]', function(event){ // #new_scenario is handled by [data-copy-link]
        var dialog = confirm_discard();
        if(dialog){
            event.preventDefault();
            var link = $(this).attr('data-discard-changes-link');
            dialog.$modal.on('hidden.bs.modal', function() {
                window.location = link
            })
        }
    });

    $('.filename input').on('change', function(){
        $(this).closest('form').trigger('submit');
    });

    //$(document).on('click', '.btn-save', function() {
    //    if ($(this).closest('form').find(':invalid').length == 0) {
    //        $('.blocking-overlay').show().find('.message').text('Working...');
    //    }
    //});

    $(document).on('mousedown', '[data-new-item-url]', function(e){
            $(this).prop('last-selected', $(this).val()); // cache old selection
    });

    $(document).on('change focus', '[data-new-item-url]', function(event){
        //this needs to ignore the event if it's in the right panel, since that will open a modal
        //#422 "Edits" in the far right will open a modal, since we've run out of space
        populate_pdf_panel(this);
    });
    
    $(document).on('click', '[data-new-item-url] + a i', function(event) {
        event.preventDefault()
        var select = $(this).closest('.control-group, td').find('select');
        populate_pdf_panel(select);

    })

    $(document).on('change', ':input, select', function(){
        $(this).closest('.layout-panel').find('.btn-save').removeAttr('disabled'); //unsaved changes
        $(this).closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
        document.getElementById("unsaved-form-header").classList.remove('hidden'); //unsaved changes
    });
    
    $(document).on('input', 'input, textarea', function(){
        $(this).closest('.layout-panel').find('.btn-save').removeAttr('disabled'); //unsaved changes
        $(this).closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
        document.getElementById("unsaved-form-header").classList.remove('hidden'); //unsaved changes
        document.getElementById("population-formset-body").classList.add('scrollbar-danger');
    });
    
    $('[data-visibility-controller]').livequery(function(){
        attach_visibility_controller(this)
    })

    
    $('[data-visibility-context]').livequery(function(){
        var context_var = window[$(this).attr('data-visibility-context')]
        if(typeof $(this).attr('data-visibility-flipped') !== 'undefined') {
            context_var = !context_var;
        }
        var hide_target = $(this).parents('.control-group')
        if (hide_target.length == 0){  //Sometimes it's not in a form group
            hide_target = $(this)
        }
        if(context_var){
            hide_target.show();
        }else{
            hide_target.hide();
        }
    });
    
    
    $("#open_file").change(function(){
        $(this).parent('form').submit();
    })

    $(document).on('click', '[data-delete-link], [additional-warning], [custom-deletable]', function(){
        var link = $(this).attr('data-delete-link')
        var deleting_outputs = typeof outputs_exist !== 'undefined' && outputs_exist;
        var do_reload = $(this).hasClass('ajax-post') || deleting_outputs
        var direct_link = $(this).hasClass('direct_link')
        var rebuild = $(this).hasClass('rebuild-list');
        var $containing_panel = $(this).closest('.layout-panel')
        var object_type = link.split('/')[2]
        if (typeof object_type === 'undefined') {
            object_type = 'object';
        }
        var additional_msg = ''
        var additional_warning = ''
        var custom_deletable = ''
        if(deleting_outputs){
            additional_msg = ' and <strong><u>All Results</u></strong>' 
        }
        if ($(this).attr('additional-warning') != undefined) {
            additional_warning = $(this).attr('additional-warning')
        }
        if ($(this).attr('custom-deletable') != undefined) {
            custom_deletable = $(this).attr('custom-deletable')
        }
        var dialog = new BootstrapDialog.show({
            title: 'Delete Confirmation',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Are you sure you want to delete the selected ' + ((custom_deletable == '') ? object_type : custom_deletable) + additional_msg + '?\n' + additional_warning,
            buttons: [
                {
                    label: 'Cancel',
                    cssClass: 'btn',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Delete',
                    cssClass: 'btn-danger',
                    action: function(dialog){
                        if(do_reload){
                            $.post(link).done(function(){
                                window.location.reload()
                            });
                        } else {
                            if(rebuild){
                                $.post(link).done(function() {
                                    dialog.close();
                                    rebuild_protocols_list();
                                });
                                return;
                            }
                            if(direct_link){
                                dialog.close();
                                window.location = link;
                                return;
                            } else {//neither tag
                                $.post(link).done(function () {
                                    clear_form_populate_panel($containing_panel, link)
                                    var newLink = '/setup/' + link.split('/')[2] + '/new/' //[2] model name
                                    var pk = link.split('/')[3];
                                    // remove option pointing to delete model
                                    $('select[data-new-item-url="' + newLink + '"] [value="' + pk + '"]').remove()
                                    dialog.close();
                                });
                            }
                        }
                        hideCenterPanel();
                    }
                }
            ]
        });
    });

    $(document).on('click', '[data-copy-link]', function(){
        var link = $(this).attr('data-copy-link')
        var dialog = check_file_saved();
        if(dialog){
            event.preventDefault();
            dialog.$modal.on('hidden.bs.modal', function() {
                prompt_for_new_file_name(link);
            })
        }else{
            prompt_for_new_file_name(link);
        }
    })

     $('#id_show_help_text').change(function(event){
        var isChecked = $(this)[0].checked;
         $.post('/app/ShowHelpText.json/', {show_help_text: isChecked}, function() {
            if(isChecked){
                $('body').removeClass('hide-help-text')
            }else{
                $('body').addClass('hide-help-text')
            }
        });
    });

    $('#id_disable_all_controls').change(function(event){
        var isChecked = $(this).prop('checked');
        var new_link = window.location;
        if(!isChecked){ //check if we're currently on a forbidden page
            var label = $('nav').find('a.active').first().text()
            $.each(['Vaccination', 'Protocol', 'Zone'], function(index, value){
                if(label.indexOf(value) != -1){
                    new_link = '/setup/VaccinationGlobal/1/'
                }
            })
        }
        safe_save('/setup/DisableAllControls.json/', {use_controls: isChecked}, new_link);
    });
    
    $(window).resize( function(){
        var nav = document.getElementById('setupMenu');  //need DOM element
        if(nav.scrollHeight > nav.clientHeight){ // returns true if there's a `vertical` scrollbar, false otherwise..
            $('#setupMenu-after, #setupMenu-before').css({'visibility': 'visible'})
        }else{
            $('#setupMenu-after, #setupMenu-before').css({'visibility': 'hidden'})
        }
    }); 
    
    $('#pop-upload').on('submit',function(event){
        var filename = $(this).find('input[type=file]').val()
        if( filename.indexOf('.xml') == -1 && filename.indexOf('.csv') == -1) {
            alert("Uploaded files must have .xml or .csv in the name: " + filename)
            event.preventDefault();
            return false;
        }
    });
    
    $('#file-upload').on('submit',function(event){
        var filename = $(this).find('input[type=file]').val()
        var valid_extensions = {"application/x-sqlite3": '.db',
                                "application/xml": '.xml'}
        var file_extension = valid_extensions[$(this).find('input[type=file]').attr('accept')]
        if( typeof file_extension !== 'undefined' && filename.indexOf(file_extension) == -1) {
            alert("Uploaded files must have "+file_extension+" in the name: " + filename)
            event.preventDefault();
            return false;
        }
    });
    $('.defined').on('click', function(){
        $('.defined').removeClass('focused')
        $(this).addClass('focused');
    });

    $('#id_equation_type').livequery(hide_unneeded_probability_fields)

    $(document).on('change', '#id_equation_type', function(){
        hide_unneeded_probability_fields();
    });

    $(document).on('click', '.edit-button', function() {
        $('.edit-button-holder a, .edit-button-holder button').addClass('reveal')
    })

    $(document).on('click', '.cancel-button', function() {
        $('.edit-button-holder a, .edit-button-holder button').removeClass('reveal')
    })

    $(document).on('click', '.overwrite-button', function () {
        make_function_panel_editable()
    })

    $('.edit-button-holder .copy-button').livequery(function() {
        $('.edit-button-holder .copy-button').on('click', function () {
            make_function_panel_editable()
            var target = $('#' + $(this).attr('form'))
            target.attr('action', target.attr('action') + 'copy/') //values already loaded, but this should go to /new/
            var name_in = $('#functions_panel #id_name')
            name_in.val(name_in.val() + ' - Copy')
        })
    })

    $('.blocking-overlay:visible').livequery( function() {
        if(window.location.pathname.indexOf('app/ImportScenario') != -1){
            if(typeof statusInterval === 'undefined'){
                statusInterval = setInterval(statusChecker, 2000);
            }
        }
    })
})

//#####################################################################################//
//#####################################################################################//

function debounce(a, b, c) {
    var d;
    return function () {
        var e = this, f = arguments;
        clearTimeout(d), d = setTimeout(function () {
            d = null, c || a.apply(e, f)
        }, b), c && !d && a.apply(e, f)
    }
};


safe_save = function(url, data, new_link){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) { 
        $.post(url, data, function() {
            if(typeof new_link === 'undefined'){
                window.location.reload();
            }else{
                window.location = new_link;
            }
        });
    } else { //confirmation dialog so we don't clobber outputs
        var dialog = new BootstrapDialog.show({
            closable: false,
            title: '',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Changing input parameters will invalidate the currently computed results. Select "Proceed" to <strong>delete the results set</strong> and commit your changes.',
            buttons: [
                {
                    label: 'Cancel',
                    cssClass: 'btn',
                    action: function(dialog){
                        window.location.reload()
                    }
                },
                {
                    label: 'Proceed',
                    cssClass: 'btn-danger btn-save',
                    action: function(dialog){
                        outputs_exist = false;
                        $.post(url, data, function(){
                            window.location.reload()
                        });
                        dialog.close()
                    }
                }
            ]
        });
    }
}

function load_target_link(callback){
        var selector = $(this).attr('load-target')

        //Wait until a problem comes up between 'active' and ':focus' to fix this
        //$input.closest('.layout-panel').find('.defined').removeClass('focused')
        //$(this).closest('.defined').addClass('focused');//?????????????????????????????????

        $(this).closest('.layout-panel').find('a').removeClass('active')  // nix .active from the earlier select
        $(this).addClass("active")  //@tjmahlin use .active to to style links between panels
        var element = this;
        $(selector).load($(this).attr('href'), function(){
            open_panel_if_needed();
            if(typeof callback === 'function'){
                callback(element);
            }
        });
        if(selector == "#center-panel") {
            $('#center-panel').addClass('reveal'); //allows toggle of box shadow on :before pseudo element
        }
    }

/*
Desc:       This function is called when the population panel (right-panel) is opened from inside the page instead of
            from the right-toolbar. It performs two actions, the first of which is to open the population panel itself,
            the second of which is to active the right-toolbar so it is clear to the user where the panel is comming
            from (and the right-toolbar button does not have to be pushed twice to clear the panel).

Params:     None

Returns:    None

Tickets:    #922 Added right-toolbar activation.
 */
function open_population_panel() {
    // get the population panel
    var pop = $('#population_panel');
    // open the population panel
    pop.removeClass('TB_panel_closed');
    pop.addClass('add-pt');
    // get the right-toolbar population button
    control = document.getElementById('TB_population');
    // activate it
    control.classList.add('active');
}

function open_panel_if_needed() {
    $('.productiontypelist, .grouplist').each(function () {
        open_population_panel();
    })
    check_if_TB_panel_form_mask_needed()
}

function populate_pdf_panel(select) {
    var $input = $(select)
    var url = $input.attr('data-new-item-url');
    if($input.hasClass('grouplist') || $input.hasClass('productiontypelist'))  //grouplist uses the population_panel instead
        return;
    var load_target = '#functions_panel #current-function'
    var origin = $input.closest('.layout-panel').attr('id');

    if(origin == 'left-panel' && (url.indexOf('RelationalFunction') == -1 && url.indexOf('ProbabilityDensityFunction') == -1)) { //use the center-panel if this is from left and not a function
        load_target = '#center-panel'
        $('#center-panel').addClass('reveal') //allows toggle of box shadow on :before pseudo element
    }
    if(load_target == '#functions_panel #current-function'){
        $('#functions_panel').removeClass('TB_panel_closed')
    }
    if(origin == 'functions_panel'){ // we've run out of room and must use a modal
        modelModal.show($input);
        return
    }
    if ($input.val() != 'data-add-new' && $input.val() != '')
        url = url.replace('new', $input.val());//will edit already existing model
    $(load_target).load(url)
    $input.closest('.layout-panel').find('select').removeClass('active')  // nix .active from the earlier select
    $input.addClass("active")  //@tjmahlin use .active to to style links between panels 
    $input.closest('.layout-panel').find('.controls').removeClass('active_linking') //made by tjmahlin - remove .active_linking from earlier select parent
    $input.parent('.controls').addClass("active_linking") //add .active_linking class to .active select parent in order to creat linking style between center and right column
}


function get_parent_select($self) {
    var parent = null
    var $inDomElement = $( '#'+ $self.find('input').last().attr('id') ) //grab the matching form from the DOM
    var actives = $inDomElement.closest('.layout-panel').prevAll('.layout-panel').first().find('select.active')
    if(actives.length){
        parent = actives.first()
    }
    return parent
}


function update_visibility_target_from_controller(disabled_value, hide_target, required_value) {
    if ($(this).val() == disabled_value && typeof disabled_value !== 'undefined') {
        hide_target.hide()
    } else {
        if ($(this).attr('type') == 'checkbox') {
            if ($(this).is(':checked') == (disabled_value === 'false')) {
                hide_target.show()
            } else {
                hide_target.hide()
            }
        }
        else {
            if (typeof required_value !== 'undefined') { //required value is specified
                if ($(this).val() == required_value || $(this).val() == '') {
                    hide_target.show()
                } else {
                    hide_target.hide()
                }
            } else {
                hide_target.show()
            }
        }
    }
}
var attach_visibility_controller = function (self){
    var controller = '[name=' + $(self).attr('data-visibility-controller') + ']'
    var hide_target = $(self).parents('.control-group')
    if (hide_target.length == 0 || $(self).attr('class') === 'help-block'){  //Sometimes it's not in a form group
        hide_target = $(self)
    }
    var disabled_value = $(self).attr('data-disabled-value')
    var required_value = $(self).attr('data-required-value')

    $('body').on('change', controller, function(){
        update_visibility_target_from_controller.call(this, disabled_value, hide_target, required_value);
    })

    //run once to initialize
    var $elem = $(controller);
    if($elem.attr('type') != 'radio' || $elem[0].hasAttribute('checked')){
        //radio buttons are multiple elements with the same name, we only want to fire if its actually checked
        update_visibility_target_from_controller.call($elem, disabled_value, hide_target, required_value);
    }
    
    $(hide_target).css('margin-left', '26px');
};


var check_file_saved = function(){
    if( $('.scenario-status.unsaved').length)
    {
        var filename = $('.filename').text().trim();
        var dialog = new BootstrapDialog.show({
            title: 'Unsaved Scenario Confirmation',
            closable: false,
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Would you like to save your changes to <strong>' + filename + '</strong> before proceeding?',
            buttons: [
                {
                    label: 'Don\'t Save',
                    cssClass: 'btn btn-dont-save',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Save',
                    cssClass: 'btn-primary btn-save',
                    action: function(dialog){
                        var form = $('.filename').closest('form');
                        $.get(form.attr('action'), $(form).serialize(),
                            function(){
                                dialog.close()
                            }
                        ).always(function() {
                            $('.blocking-overlay').hide();
                        })
                    }
                }
            ]
        });
        return dialog;
    }
};


var confirm_discard = function(){
    if( $('.scenario-status.unsaved').length)
    {
        var filename = $('.filename').text().trim();
        var dialog = new BootstrapDialog.show({
            title: 'Discard Changes Confirmation',
            closable: false,
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Are you sure you would like to discard your changes to <strong>' + filename + '</strong>?',
            buttons: [
                {
                    label: 'Discard Changes',
                    cssClass: 'btn btn-dont-save',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Cancel',
                    cssClass: 'btn-primary btn-save',
                    action: function(dialog){
                        dialog.$modal.hide();
                        $('.modal-backdrop').hide();
                        return false;
                    }
                }
            ]
        });
        return dialog;
    }
};


two_state_button = function(){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) {
        return 'class="btn btn-primary btn-save" formnovalidate >Apply changes'
    } else {
        return 'class="btn btn-danger btn-save" formnovalidate >Delete Results and Apply Changes'
    }
}


function contains_errors(html) {
    return $(html).find('span.error-inline').length
}

function add_model_option_to_selects(html, selectInput) {
    var action = $(html).find('form').first().attr('action');
    if(!action) { //sometimes this gets called for things that aren't a model option
        return;
    }
    var pk = action.split('/')[3]; //the edit action URL has the pk in it
    var model_link = action.replace(pk, 'new'); //for targetting other selects
    var title = 'Newest Entry';
    try {
        title = $(html).find('input[type="text"]').first().val();
    } catch (e) { }

    $('select[data-new-item-url="' + model_link + '"] [value="data-add-new"]')
        .before($('<option value="' + pk + '">' + title + '</option>')); // Add option to all similar selects
    if(selectInput != null){
        selectInput.val(pk); // select option for select that was originally clicked
        selectInput.closest('.layout-panel').find('.btn-save').removeAttr('disabled'); //unsaved changes
        parent_select.closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
        selectInput.closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
        document.getElementById("unsaved-form-header").classList.remove('hidden'); //unsaved changes
    }
    //add functions to their panel lists
    var $new_link = $('.function_dropdown [href="' + model_link + '"]')
    if($new_link.length) {
        var $back_link = $new_link.clone()
        $back_link.attr('href', $back_link.attr('href').replace('new', pk))
        $back_link.text(title)
        $new_link.parent().after($('<li>' + $back_link.prop('outerHTML') + '</li>')); // Add new link with all properties
    }
}

var modelModal = {
    //processData: false,
                //contentType: false}
    ajax_submit: function(url, success_callback, fail_callback){
        var $form = $('.modal-body form')
        return $.ajax({
            url: url,
            type: "POST",
            data: new FormData($form[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: function(html) {
                if (contains_errors(html)) { //html dataType  == failure probably validation errors
                    fail_callback(html)
                } else {
                    success_callback(html)
                }
            }
        }).always(function() {
            $('.blocking-overlay').hide();
        });
    },

    ajax_success: function(modal, selectInput){
        return function(html) {
            add_model_option_to_selects(html, selectInput);
            modal.modal('hide');
        };
    },

    populate_modal_body: function($newForm, modal) {
        //$form.find('.buttonHolder').remove();
        modal.find('.modal-title').html($newForm.find('#title').html());
        modal.find('.modal-body').html($newForm.find('form').first());
        //modal.find('.modal-footer').html($newForm.find(".buttonHolder"))
        $('body').append(modal);
    },

    validation_error: function(modal) {
        var self = this;
        return function(html) {
            console.log('validation_error:\n');
            self.populate_modal_body($(html), modal);
        };
    },

    show: function($selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', $selectInput.attr('name') + '_modal');
        var url = $selectInput.attr('data-new-item-url');
        if($selectInput.val() != 'data-add-new' && $selectInput.val() != '')
            url = url.replace('new', $selectInput.val());//will edit already existing model

        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));
            self.populate_modal_body($newForm, modal);
            modal.find('.modal-footer button[type=submit]').on('click', function() {
                self.ajax_submit(url, self.ajax_success(modal, $selectInput), self.validation_error(modal));
            });

            modal.modal('show');
            $(modal).on('hidden.bs.modal', function(){
                $(this).remove(); // deletes it from the DOM so it doesn't get cluttered
            })
        });

        },
    
    template: $('<div class="modal fade">\
                  <div class="modal-dialog layout-panel">\
                    <div class="modal-content">\
                      <div class="modal-header">\
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                        <h4 class="modal-title"></h4>\
                      </div>\
                      <div class="modal-body">\
                      </div>\
                      <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                            <button type="submit"' + two_state_button() + '</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}

function check_disabled_controls() {
    /*Disables all the inputs on the Control Master Plan if the disable_all check box is checked on page load */
    if (typeof controls_enabled !== 'undefined' && !controls_enabled && $('#id_destruction_program_delay').length) { //global from context processor
        $('.layout-panel form').first().children('div:not(#div_id_name)').each(function (index, value) {
            $(value).attr('disabled', 'disabled')
            $(value).find(':input').attr('disabled', true);
        });
    }//else do nothing
};

function reload_model_list($form) { //TODO: change this to expect a fragment
    $('#left-panel').load(window.location + " #left-panel>*, script");
    if(typeof $form !== 'undefined'  && $form.length){
        var action = $form[0]['action']; //.attr('action');
        if(action.indexOf('ProductionGroup') != -1){
            $('#production_group_container').load("/setup/PopulationPanel/ #production_group_container>*")  //new address for ajax loading
            //#707 Fix by loading only the production group section dynamically
        }
    }
}

function check_if_TB_panel_form_mask_needed(){  // I'm currently assuming that all forms are coming from the [load-target] attribute
    var button = $('.TB_panel form .btn-cancel')  //cancellable form was the most specific thing I could think of
    if(button.length && button.closest('form').length){
        var $form = $(button.closest('form'))
        $('.panel-backdrop').show()
        $form.find('.btn-cancel').click(function(){$('.panel-backdrop').hide()})
        $form.find('.btn-save').click(function(){$('.panel-backdrop').hide()})
        $form.closest('.TB_panel').css('z-index', 1050)  // can't seem to bring out a smaller sub component with z-index
    }
}

function prompt_for_new_file_name(link) {
    var is_current_scenario = link == '/app/SaveScenario/'
    var dialog = new BootstrapDialog.show({
        title: 'Scenario Save As...',
        type: BootstrapDialog.TYPE_PRIMARY,
        message: '<div>Enter the name of the new scenario: <input type="text" id="new_name"></div><div>WARNING: Supplying a name of a Scenario that already exists in your ADSM Workspace will OVERWRITE the existing Scenario!</div>',
        buttons: [
            {
                label: 'Cancel',
                cssClass: 'btn',
                action: function (dialog) {
                    dialog.close();
                }
            },
            {
                label: 'Save As',
                cssClass: 'btn-primary',
                action: function (dialog) {
                    dialog.close();
                    var $self = $('.filename input').closest('form');
                    if (is_current_scenario) {
                        $('.filename input').val($('#new_name').val())
                        //$self.submit()
                        ajax_submit_complex_form_and_replaceWith(link, new FormData($self[0]), $self, $self, undefined, function () {
                            $('h1.filename').text($('.filename input').val()) //match major title with form value
                        });
                        location.reload();
                    } else {
                        //TODO: need FormData from form that is to be added in #NewScenario
                        //ajax_submit_complex_form_and_replaceWith(link, new FormData($self[0]), $self, $self, undefined);

                        window.location = link + $('#new_name').val();
                    }
                }
            }
        ]
    });
}

function clear_form_populate_panel($container_panel, delete_link) {
    if($container_panel.hasClass('layout-panel') == false //not a layout-panel
            && $container_panel.closest('.layout-panel').attr('id') != 'population_panel') { //inside function panel or left-panel
        $container_panel = $container_panel.closest('.layout-panel') //upgrade to function panel
    }
    var panel_id = $container_panel.attr('id');
    if (panel_id == 'functions_panel') {
        //load list of functions instead of blank
        $.get('/setup/Function/', function (newForm) {
            var $newForm = $($.parseHTML(newForm));
            $container_panel.html($newForm)
        })
    } else {
        if(panel_id == 'left-panel') {
            reload_model_list();
            var primary_key = delete_link.split('/')[3];
            var $center_form = $('#center-panel').find('form');
            if( $center_form.length){
                if(typeof delete_link !== 'undefined' && $center_form.attr('action').indexOf(primary_key) != -1){
                    $('#center-panel').html('')
                }
            }
        } else { //will still clear Create Group form inside of population_panel without destroying the whole panel
            $container_panel.html('') //delete everything from the div containing the form
        }
    }
}


function reload_image(load_target) {
    var target = load_target.find('form')
    if(target.hasClass('relational-form') || target.hasClass('probability-form')){
        var img = $('#function-graph'); //newly placed image
        d = new Date();
        var new_src = img.attr("src") + "?" + d.getTime();
        img.attr("src", new_src);
    }
}

function ajax_submit_complex_form_and_replaceWith(formAction, formData, $self, load_target, loading_message, success_callback) {
    var overlay = $('.blocking-overlay').show();
    if(typeof loading_message !== 'undefined'){
        overlay.find('.message').text(loading_message);
    }
    $.ajax({
        url: formAction,
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function (form_html) {
            $('.scenario-status').addClass('unsaved')
            // Here we replace the form, for the
            if ($self.closest('#main-panel').length) { //in the main panel, just reload the page
                if($(form_html).find('#main-panel').length ){
                    $('#main-panel').replaceWith($(form_html).find('#main-panel')[0])
                }else {
                    var contents = $(form_html).find('#layout-container');
                    if( !contents.length ){
                        contents = $('<div/>').html(form_html).find('#layout-container');
                        if( !contents.length ){ // double redundant backup in case someone doesn't define layout-container
                            var matches = form_html.match(/(<body.*>[\S\s]*<\/body>)/i);//multiline match
                            if(matches){
                                var content = $(matches[1]);
                                $('body').html(content);
                                return; // this method doesn't play well with others
                            }
                        }
                    }
                    $('#layout-container').replaceWith(contents[0]);
                }
            } else {
                var parent_panel = $self.closest('.layout-panel').attr('id');
                if((parent_panel == 'center-panel' || parent_panel == 'population_panel') ){
                    if(window.location.pathname.indexOf('setup/ControlProtocol/') != -1) {
                        rebuild_protocols_list();
                    }else {  // don't do this on ControlProtocol pages
                        reload_model_list($self); //reload left
                    }
                }else{
                    var lastClickedSelect = get_parent_select($self);
                    add_model_option_to_selects(form_html, lastClickedSelect);
                }
                load_target.replaceWith(form_html);
                reload_image(load_target)
            }
            if(typeof success_callback === 'function'){
                success_callback()
            }
        },
        error: function () {
            $self.find('.error-message').show()
        }
    }).always(function () {
        $('.blocking-overlay').hide();
    });
}

function hide_unneeded_probability_fields() {
    var $idEquationType = $('#id_equation_type');
    var equation_type = $idEquationType.val()
    var fields = $idEquationType.closest('.control-group').nextAll('.control-group');
    fields.each(function (index, control_group) {
        var help_text = $(control_group).find('.help-block').first().text();
        var functions = help_text.toLowerCase().match(/(\w[\w\s]*)(?=[,\.])/g);
        if (functions.indexOf(equation_type.toLowerCase()) >= 0) {
            $(control_group).show();
            $(control_group).find(':input').attr('required', 'required'); //this code is mirrored in the django form validation
        }
        else {
            $(control_group).hide();
            $(control_group).find(':input').removeAttr('required');
        }
    });
}

function make_function_panel_editable() {
    $('.edit-button-holder a, .edit-button-holder button').removeClass('reveal') //collapse the edit buttons, possibly hide
    $('.edit-button-holder').css('display', 'none')
    $('.back-button').css('display', 'none')

    var base = $('#functions_panel');
    var $modal = $('.modal-body');
    if($modal.length > 0) base = $modal
    base.find('.buttonHolder').removeAttr('hidden')
    base.addClass('editable')
    base.find('input').addClass('editable').removeAttr('disabled')
    base.find('select').addClass('editable').removeAttr('disabled')
    base.find('textarea').addClass('editable').removeAttr('disabled')
    base.find(':input').addClass('editable')
    //$('#tb_mask').css('visibility', 'visible')
    base.css('pointer-events', 'all')
}

function statusChecker(){
    if($('.blocking-overlay').is(':visible')){
        $.get('/app/ImportStatus/', function(data){
            $('.blocking-overlay').show().find('.message').text(data.status);
        });
    }else{
        clearInterval(statusChecker);
    }
}

function rebuild_protocols_list() {
    $('#protocol_list #accordion').remove();
    build_protocols_list(); // build from js rather than reload HTML
}

function hideCenterPanel() {
    center_panel = document.getElementById("center-panel");
    if (center_panel != null) {
        center_panel.classList.remove("reveal");

        // Next two loops is for un-focusing user disease spreads when the center panel is closed.
        var active_list_elements = document.getElementsByClassName("defined_name");
        for (var i = 0; i < active_list_elements.length; i++) {
            $(active_list_elements[i]).removeClass("active");
        }
        var active_list_div = document.getElementsByClassName("defined");
        for (var i = 0; i < active_list_div.length; i++) {
            $(active_list_div[i]).removeClass("focused");
        }
    }
}

function hideFunctionsPanel() {
    // Click the back button on the functions panel.
    document.getElementsByName("functions_back")[0].click();

    let functions_panel = document.getElementById('functions_panel');
    functions_panel.classList.add("TB_panel_closed");

    let toolbar_btn = document.getElementById("TB_functions");
    toolbar_btn.classList.remove('active');
}

function show_crash_text(error_text) {
    var dialog = new BootstrapDialog.show({
        title: 'Simulation Error Details',
        type: BootstrapDialog.TYPE_WARNING,
        message: error_text,
        buttons: [
            {
                label: 'Return to Scenario Creator',
                cssClass: 'btn-primary',
                action: function (dialog) {
                       location.replace("/results/Inputs/");
                }
            }
        ]
    });
}