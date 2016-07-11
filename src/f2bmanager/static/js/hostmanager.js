$(document).ready(function() {
        edit_name = ''
        $('button.viewbutton').click(function() {
          edit_name = $(this).parent().parent().find('.nametd').text();
           window.location.href = "http://127.0.0.1:8000/viewlog?name="+edit_name;
        });
        $('button.getbutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            $.ajax({
              url: "http://127.0.0.1:8000/getlog",
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
            window.location.href = "http://127.0.0.1:8000/edithost?name="+edit_name;
        });
        $('button.deletebutton').click(function() {
            edit_name = $(this).parent().parent().find('.nametd').text();
            elem = $(this).parent().parent();
            $.ajax({
              url: "http://127.0.0.1:8000/deletehost",
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