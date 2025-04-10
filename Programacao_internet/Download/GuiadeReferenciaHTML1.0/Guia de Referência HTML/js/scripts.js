$(function(){
	
	$("div.cab").click(function(){
		$(this).parent().find(".info").toggle(200);
	});
	
	$("code.hide").before('<span class="exemplo" title="Exibir/esconder exemplo"></span>');
	$("code.hide").each(function(index, element) {
        $(this).css("display", "none");
		$(this).parent().find("samp").css("display", "none");
    });
	$("span.exemplo").click(function(){
		$(this).parent().find("code, samp").toggle(200);
	});
	
	$("#selMenu").change(function(){
		var alvo = $(this).val();
		if ( alvo != "0" ) {
			location.href = "#" +alvo;
			$(this).val("0");
		}
	});
	
});