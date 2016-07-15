$(document).ready(function() {
        edit_name = ''
        $('button.viewbutton').click(function() {
           edit_name = $(this).parent().parent().find('.nametd').text();
           window.location.href = "/viewcustomaction?name="+edit_name;
        });
        $('button.editbutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            window.location.href = "/editcustomaction?name="+edit_name;
        });
        $('button.deletebutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            elem = $(this).parent().parent();
            $.ajax({
              url: "/deletecustomaction",
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