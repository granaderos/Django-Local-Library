$(function () {
    //alert("Script is working")
    $('[data-toggle="tooltip"]').tooltip();

    $(".datepicker").datepicker();
  });

function author_delete(id) {
  //{% url 'author-delete' author.id %}
  //alert("clicked");
  //$("#popup_div").dialog({model: true});
}