$(function () {
    //alert("Script is working")
    $('[data-toggle="tooltip"]').tooltip();
    //$("#datepicker").datepicker();
    //$(".datepicker").datepicker();

  $("#book_keyword").keyup(function(e) {
    search_book(e);
  });

  $("#form_search_book").submit(function(e) {
    search_book(e);
  });

});

function search_book(e) {
  e.preventDefault();
  var th_book_action = document.getElementById("th_book_action");
  $.ajax({
    type: "GET",
    url: "search_book",
    data: $("#form_search_book").serialize(),
    success: function(data, textStatus) {
      console.log("Success: " + JSON.stringify(data) + " : " + textStatus);
      console.log("Success 1: " + data)
      var parsed_data = JSON.parse(data);
      console.log("parse_data = " + JSON.stringify(parsed_data))
      var display = "";
      if(parsed_data.length > 0) {
        for(var i = 0; i < parsed_data.length; i++) {
          console.log("d["+i+"] = " + parsed_data[i]);
          console.log(parsed_data[i].pk);
          display += 
            "<tr>" +
                "<td><a href='/catalog/book/"+parsed_data[i].pk+"'>" + parsed_data[i].title + "</a></td>" +
                "<td>" + parsed_data[i].author + "</td>";
            if(th_book_action) {
              display += "<td>" +
                  "<a href='/catalog/book/"+ parsed_data[i].pk +"/update/' data-toggle='tooltip' data-placement='top' title='Edit book information.'><span class='fa fa-edit'></span></a> | " + 
                  "<a href='/catalog/book/" + parsed_data[i].pk + "/delete/' data-toggle='tooltip' data-placement='bottom' title='Delete this book.'><span class='fa fa-trash-alt'></span></a>" +
              "</td>";
            }

            display += "</tr>";
        }

      } else {
        display = "<p class='alert alert-danger'>No results found;</p>"
      }
      
      $("#tbody_book_list").html(display);
      $(".pagination").hide();
    },
    error: function(data) {
      console.log("Error in searching book: " + JSON.stringify(data))
    }
  });
}

function author_delete(id) {
  //{% url 'author-delete' author.id %}
  //alert("clicked");
  //$("#popup_div").dialog({model: true});
}