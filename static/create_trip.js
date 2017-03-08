// This is JS to create new trip
// $("#mylink").on("click", function(evt) {
//   evt.preventDefault();
//   $(".col-xs-12").attr("style", "display:inline");

// });

// $("#minimize").on("click", function(evt) {
//   $(".col-xs-12").attr("style", "display:none");
// });

$(".tripform").on('click', function() {
  submitTrip(evt);
  // $("#myModal").modal('hide');

});


function submitTrip(evt) {
  evt.preventDefault();
  // var tripcode = $("#tripc").val()
  var tripname = $("#tripn").val();
  tripData = {"tripname": $("#tripn").val(),
              "datestart": $("#sdate").val(),
              "numdays": $("#numdays").val()};


  $.post("/new_trip", tripData, function(response) {
    my_response = JSON.parse(response);
    console.log(my_response);
    tripCode = my_response["tripCode"];
    console.log(response);
    console.log(tripCode);
    var new_line = "<li><a href='/trip_detail/"+tripCode+"'>"+tripname+"</a></li>";
    $("#new_trip").before(new_line) ;});
    // $("#myModal").modal('hide');
}