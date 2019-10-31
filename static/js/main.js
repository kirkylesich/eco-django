
$(function() {
	if (typeof jQuery != 'undefined') {console.log(jQuery.fn.jquery);}

});

$('.showPass').click(function() {
	$('.userPassInput').prop('type', $(this).data( "type" ));
});