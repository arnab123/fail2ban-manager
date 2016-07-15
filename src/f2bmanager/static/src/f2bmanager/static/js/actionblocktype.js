var e = document.getElementById("id_block_type");
var str = e.options[e.selectedIndex].text;
console.log(str);
console.log('hi');
if(str=="Iptables"){
	var elems = document.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bt' + ' ') > -1) {
            if((' ' + elems[i].className + ' ').indexOf(' ' + 'ip' + ' ') < 0) {
            	elems[i].style.display = 'none';
            }
        }
    }
}
else if(str=="TCP-Wrapper"){
	var elems = document.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bt' + ' ') > -1) {
            if((' ' + elems[i].className + ' ').indexOf(' ' + 'tcp' + ' ') < 0) {
            	elems[i].style.display = 'none';
            }
        }
    }
}
else {
	for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bt' + ' ') > -1) {
            	elems[i].style.display = 'none';
            
        }
    }
}

$(document).on('change','#id_block_type',function(){
        var e = document.getElementById("id_block_type");
		var str = e.options[e.selectedIndex].text;
		if(str=="Iptables"){
			$(".bt").each(function() {
			    $(this).hide()
			});
			$(".ip").each(function() {
			    $(this).show()
			});
		}
		else if(str=="TCP-Wrapper"){
			$(".bt").each(function() {
			    $(this).hide()
			});
			$(".tcp").each(function() {
			    $(this).show()
			});
		}
		else{
			$(".bt").each(function() {
			    $(this).hide()
			});
		}
    });


