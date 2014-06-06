/** Javascript widget designed to make many group assignments as quick and painless as possible.
 * Described in https://github.com/NAVADMC/SpreadModel/issues/77.
 * Used in Disease Spread Assignment and Zone assignment.
 * Possibly could be used in Assigning Progression and Protocols as well.
 * Created by Josiah and Marshall on 6/5/14.
 */
var form_state;
var many_to_many_widget;
var form_prefix = /form-(\d+)-/g;

function headerify_columns1_2() {
    $('tbody tr td:nth-child(-n+2)').replaceWith(function (i, html) {
        return '<th>' + html + '</th>';
    });
}

$(function(){

//state object
form_state = (function(form){
    var state = {};
    //load done by views.py queryset
    //list Assignments already in DB
    //serialize -> POST
    //get(source destination)

    var format_form_array = function(serialized_array){
        var row = {};
        $.each(serialized_array, function(index, container){
            var name = container.name.replace(form_prefix, "")
            row[name] = container.value;
            row['form_number'] = form_prefix.exec(container.name)[1]
        });
        return row;
    };

    /*Gets all the rows in the formset that matches 'filters' criteria*/
    var get = function(filters){
        if(typeof filters != "object"){
            throw new TypeError("Must be an object containing, (field, value) pairs");
        }
        var matching_row = [];
        form.find('tbody tr').each(function(){
            var row_data = format_form_array($(this).find(':input').serializeArray());
            var pass = true;
            $.each( filters, function( key, value ) {
                if(!row_data.hasOwnProperty(key))
                    return pass = false;
                else if(row_data[key] != value)
                    return pass = false;
            })// we have gotten through all filters with matching value == test passed
            if( pass ){
                matching_row.push(row_data);
            }
        });
        return matching_row
    };

    //This will set all rows that meets the filters criteria.  You can pass in multiple input variables
    //to be set in that row.
    var set = function(filters, variables){
        if(typeof filters != "object" || typeof variables != "object"){
            throw new TypeError("Must be an object containing, (field, value) pairs");
        }

        $.each(get(filters), function(index, row){
            var matching_row_number = row['form_number'];
            for(var key in variables){
                var input_name = 'id_form-' + matching_row_number + '-' + key;
                $('#'+input_name).val(variables[key]);
            }
        })
    };

    return {
        'save': function(){$.post('', form.serialize())},
        'get':  get,
        'set':  set
    };
})($('section form'));



many_to_many_widget = (function(form_state){
    var my_table;
    //jquery events
        //select change
    //render
    function insert_select_buttons() {
        var select_buttons = '<td><button class="mtm-button select-all">Select All</button>' +
            '<button class="mtm-button deselect">Deselect All</button></td>'
        my_table.find('thead').append($('<tr>').append(select_buttons).append(select_buttons))
    }

    function insert_bulk_selectors() {
        $('section form table tbody tr:last-child td').each(function (index) {
            if (index > 1) {//3D: we want to skip the first two columns (source, destination)
                var bulk_select = $(this).find('select').clone()
                bulk_select.attr('id', bulk_select.attr('id').replace(form_prefix, 'bulk-')).val("");
                my_table.find('thead tr:nth-child(2)').append($('<td>').append(bulk_select)); //sensitive selector
            }
        });
    }

    function extract_options(index, element){//grab each option and generate row
        var value = $(element).attr('value');
        if(value && value != 'data-add-new'){//not "-----" or "Add..."
            return [[$(element).text(), value]];
        }
    }

    function render_row(column_information, row_index){
        var row = $('<tr>')
        $.each(column_information, function(col_index, column){//for each column
            var td = $('<td>');
            if(col_index < 2){
                td.append('<span data-click-toggle="selected" data-pk="'+ column[row_index][1] + '">' + column[row_index][0] + '</span>'); //column contains row list
            }
            else if(column_information[1][row_index]){ //check if there's something in the second column (could be ragged)
                td.append(column.clone()); // column contains select
            }
            row.append(td);
        })
        return row;
    }

    function create_body_rows() {
        var tbody = $('<tbody>');
        var column_information = []
        $('section form table tbody tr:last-child td').each(function (index) {
            if (index < 2) {//first two columns
                column_information[index] = $(this).find('option').map(extract_options)
            }
            else {//for remaining columns, copy the select
                column_information[index] = $(this).find('select').clone().val('')// you will need to scrub id and name later
            }
        });
        var num_rows = Math.max(column_information[0].length, column_information[1].length) //
        for (var i = 0; i < num_rows; i++) {
            tbody.append(render_row(column_information, i))
        }
        return tbody;
    }

    function get_column_name(column_index){
        var print = $('section form table thead tr:nth-child(1) th:nth-child('+column_index+')').text()
        return print.toLowerCase().replace(/\s/g, "_")
    }
    var render = function(){
        my_table = $('<table>').append($('section form table thead').clone());
        insert_select_buttons();
        insert_bulk_selectors();
        my_table.append(create_body_rows())
        update_data() //called from events normally, but we want to initialize

        $('section form').before(my_table); //finally, insert everything into the DOM
    };

    /*Ensures that the state of the displayed widget is consistent with form_state for the appropriate
    * row / column pairs.*/
    function update_data(){
        my_table.find('tbody tr').each(function(row_index, row){
            var filter = {}
            $(row).find('td').each(function(column_index, column){
                var column_name = get_column_name(column_index+1);//column name
                if(column_index < 2){
                    var value = $(column).find('span').attr('data-pk');
                    filter[column_name] = value;
                } else {
                    var row_values = form_state.get(filter)[0]; //we only need the first match (should only be one)
                    console.log(row_values)
                    $(column).find(':input').val(row_values[column_name]) //set the select to the matching formset select
                }
            })
        })
    };


    //bulk apply
    //select source
    //select destination
    //main selects under bulk need an event watcher for incongruous source values == "varies" <option>
    //draw arrows

    return {
        'render': render,
        'get_column_name': get_column_name,
        'update_data': update_data
    }
})(form_state)

//    headerify_columns1_2();
    many_to_many_widget.render();
});

