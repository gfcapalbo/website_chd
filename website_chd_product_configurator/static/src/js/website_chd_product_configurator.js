$(document).ready(function ()
	{
	$('.type_selection').on('change', function ()
    {	var website = openerp.website;
		return website.session.model('product.finishing').call('search_read', [], {
		    domain: [['type_option_ids', 'in', [this.value]]],
		    fields: ['id', 'name'],
		    limit: 30,
		}).then(function(finishings)
				{	debugger;
					$('#fini_select_id').empty();
					$('#fini_select_id').append("<option></option>");
					for (i = 0; i < finishings.length; i++) {
							$('#fini_select_id').append("<option value='" + finishings[i].id + "'>"+ finishings[i].name + "</option>");
					}
				})
    });




	$('#mainf input, #mainf select').each(function()
			{
			var element=this;
			$(element).on('change', function()
					{
						$('#mainf input, #mainf select').each(function()
								{	var feedback_container = null;
									if (document.getElementById("error_msg")){
										document.getElementById("error_msg").innerHTML="";
									}
									var rawname = element.name;
									var name = rawname.split("_");


									if (document.getElementById("div_" + rawname)) {
										var currdiv = (document.getElementById("div_" + rawname));
										currdiv.innerHTML = "";

									} else {
										var currdiv = document.createElement("div");
										jQuery(currdiv).attr({id: "div_" + rawname, class: 'quotation'});
									}
									var value = element.value;
									if (element.nodeName=="SELECT") {
											value=element[element.selectedIndex].label;
									}
									if (name.length > 2){
										if (name[0] == 'qtyaccessoryid') {
											if (value > 0){
												var newcontent = document.createTextNode(name[2] +" : " + value);
											}
										}else if (name[0] == 'pricecomponent') {
											var newcontent = document.createTextNode(name[4] +" : " + value);}
									} else {
										var newcontent = document.createTextNode(rawname +" : " + value);
										}
									if (newcontent){
										currdiv.appendChild(newcontent);
										if (name[0] == 'qtyaccessoryid') {
											var feedback_container= document.getElementById("accessory_preferences");

										} else {
											var feedback_container= document.getElementById("preferences");
										}
										feedback_container.appendChild(currdiv);
									}

							});
				});
			});


	//added after on submit , with the rest of the form fields.
	$("#mainf").submit( function()
		        {
		 			var elements = document.querySelectorAll( 'feedback *' );
		 			$('<input />').attr('type', 'hidden')
			         .attr('name', "summary")
			         .attr('value', document.getElementById("feedback").innerHTML)
			         .appendTo('#mainf');
    	             return true;
		        });

	$('.result_option').submit( function()
			{
				chosenform=this;
	 			var elements = document.querySelectorAll( 'feedback *' );
	 			$('<input />').attr('type', 'hidden')
		         .attr('name', "summary")
		         .attr('value', document.getElementById("feedback").innerHTML)
		         .appendTo(chosenform);
	             return true;
	        });

	 $(".back").click(function ()
			 {
	     		window.history.back();
			 });

});

