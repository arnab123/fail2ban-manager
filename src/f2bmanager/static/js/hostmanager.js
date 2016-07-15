$(document).ready(function() {
        edit_name = ''
        $('button.viewbutton').click(function() {
          edit_name = $(this).parent().parent().find('.nametd').text();
           window.location.href = "/viewlog?name="+edit_name;
        });
        $('button.getbutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            $.ajax({
              url: "/getlog",
              method: 'GET',
              data: {
                  name: edit_name,
              },
              success: function (response) {
                  console.log("success")
                  console.log(new Date().toLocaleString())
              }
            });
        });
        $('button.editbutton').click(function() {
          edit_name = $(this).parent().parent().find('.nametd').text();
            window.location.href = "/edithost?name="+edit_name;
        });
        $('button.deletebutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            elem = $(this).parent().parent();
            $.ajax({
              url: "/deletehost",
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