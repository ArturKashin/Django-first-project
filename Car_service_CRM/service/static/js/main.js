$(document).ready(function(){

	add__order_display();
	add__work_order();


//окно добавление наряда
	$('#add_order').click(function(){
		if($('#add_order').is(':checked')){
			$('.add_order').css({'display':''});
			$('.add_ord').css({'color': 'red', 'font-weight': '600'});
		}else{
			$('.add_order').css({'display':'none'});
			$('.add_ord').css({'color': 'black', 'font-weight': '400'});
		}
	})
	
	function add__order_display(){
		if($('#add_order').is(':checked')){
			$('.add_order').css({'display':''});
		}else{
			$('.add_order').css({'display':'none'});
		}
	}
	
	
//	окно добавления работ к наряду
	$('#add_work').click(function(){
		if($('#add_work').is(':checked')){
			$('.add_work').css({'display':''});
			$('.add_works').css({'color': 'red', 'font-weight': '600'});
		}else{
			$('.add_work').css({'display':'none'});
			$('.add_works').css({'color': 'black', 'font-weight': '400'});
		}
	})

	function add__work_order(){
		if($('#add_work').is(':checked')){
			$('.add_work').css({'display':''});
		}else{
			$('.add_work').css({'display':'none'});
		}
	}
	
	
	
});