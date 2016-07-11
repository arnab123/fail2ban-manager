$(document).ready(function() {
        edit_name = ''
        $('button.viewbutton').click(function() {
           edit_name = $(this).parent().parent().find('.nametd').text();
           window.location.href = "http://127.0.0.1:8000/viewcustomaction?name="+edit_name;
        });
        $('button.editbutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            window.location.href = "http://127.0.0.1:8000/editcustomaction?name="+edit_name;
        });
        $('button.deletebutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            elem = $(this).parent().parent();
            $.ajax({
              url: "http://127.0.0.1:8000/deletecustomaction",
              method: 'GET',
              data: {
                  name: edit_name,
              },
              success: function (response) {
                  elem.hide();
              }
          });
        });
    });