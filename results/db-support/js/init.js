$(document).ready(function(){

function populate() {

	if($('#state').val() == 'AK' || $('#state').val() == 'DC') // Alaska and District Columbia have no counties
    {
       $('#county_drop_down').hide();
       $('#no_county_drop_down').show();
    } else {
       fetch.doPost('getCounties.php');
	}
}

$('#state').change(populate);

var fetch = function() {
		
var counties = $('#county');
return {
	doPost: function(src) {

    $('#loading_county_drop_down').show(); // Show the Loading...
    $('#county_drop_down').hide(); // Hide the drop down
    $('#no_county_drop_down').hide(); // Hide the "no counties" message (if it's the case)


		if (src) $.post(src, { state_code: $('#state').val() }, this.getCounties);
		else throw new Error('No SRC was passed to getCounties!');
	},
			
	getCounties: function(results) {
		if (!results) return;
		counties.html(results);

	$('#loading_county_drop_down').hide(); // Hide the Loading...
	$('#county_drop_down').show(); // Show the drop down
	}	
}
}();

populate();

});