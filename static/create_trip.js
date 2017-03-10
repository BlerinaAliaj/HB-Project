// This is JS to create new trip

$(".tripform").on('submit', submitTrip);

function submitTrip(evt) {
  evt.preventDefault();
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
    document.getElementById("ntform").reset();
}