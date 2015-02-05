$(document).ready(function () {


	$('.favorites_option').submit( function(){
		chosenform=this;
			var elements = document.querySelectorAll( 'feedback *' );
			var accessories
			$('<input />').attr('type', 'hidden')
         .attr('name', "summary")
         .attr('value', document.getElementById("feedback").innerHTML)
         .appendTo(chosenform);
         return true;
    });


	$(".back").click(function () {
		window.history.back().refresh();

	});

	$(".erase").on("click", null, function(){
        return confirm("Are you sure you want to permanently delete this element?");
	});

});