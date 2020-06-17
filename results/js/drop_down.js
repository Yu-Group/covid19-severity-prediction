function drop_down_list()
{
    var state = $('#state').val();

    if(state == 'AK' || state == 'DC') // Alaska and District Columbia have no counties
    {
    $('#county_drop_down').hide();
    $('#no_county_drop_down').show();
    }
    else
    {
    $('#loading_county_drop_down').show(); // Show the Loading...
	
    $('#county_drop_down').hide(); // Hide the drop down
    $('#no_county_drop_down').hide(); // Hide the "no counties" message (if it's the case)

    $.getScript("js/states/"+ state.toLowerCase() +".js", function(){

    populate(document.form.county);

 	$('#loading_county_drop_down').hide(); // Hide the Loading...
	$('#county_drop_down').show(); // Show the drop down
    });
}
}
function findplot()
{
    var state = $('#state').val();
    var county = ""
    if(state != 'AK' && state != 'DC') // Alaska and District Columbia have no counties
    {
    county = $('#county').val();
    }
    return state;
    
}
$(document).ready(function(){
$("#state").change(drop_down_list);
});

$(window).load(drop_down_list);
