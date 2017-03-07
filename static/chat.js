// Script for socketIO real time messaging

$(document).ready(function() {

  var socket = io.connect('localhost:5000');

  socket.on('connect', function () {
    console.log("connected and about to join room %s", tripCode);
    console.log(socket);
    socket.emit('join', tripCode);
  });


socket.on('message', function(msg) {
  $("#messages").append('<li class="right clearfix"><span class="chat-img pull-right"><img src="http://placehold.it/50/FA6F57/fff&text=ME" alt="User Avatar" class="img-circle"/></span><div class="chat-body clearfix"><div class="header"><small class=" text-muted"><span class="glyphicon glyphicon-time"></span>13 mins ago</small><strong class="pull-right primary-font">'+ userid + '</strong></div><p>' + msg +'</p></div></li>');
  console.log('Received message');
});

$('#sendbutton').on('click', function() {
  console.log($("#mytext.form-control").val());
  socket.emit('json', { "msg": $("#mytext.form-control").val(), "room": tripCode});
  $("#mytext.form-control").val(''); }); });

//JQuery to update messages

// $.get("/message.json/"+trip_code, updateMessage);

// function updateMessage(data) {
//   if (data) {
//     for (var key in data) {
//       var message = data[key].message;
//       var user = data[key].user;
//       var time = data[key].timestamp;
//       $("#message").append("<li>"+ message + ", sent by: "+ user + "</li>");

//     }
//   } else {
//     $("#message").append("<li> No messages Logged Yet.</li>");
//   }
// }

// function sendMessage(evt){
//   evt.preventDefault();

//   var newMessage = $("#mytext").val();
//   console.log(newMessage);
//   messages = { "message": newMessage,
//                "trip_code":  trip_code};

//   $.post("/message", messages, function() { $("#mytext").val("");
//     $("#message").append("<li>"+ newMessage + ", sent by: " +username+ "</li>"); });
// }

// $("#sendmessage").on('submit', sendMessage);


// setInterval(function(){
//     $.get("/message.json/"+trip_code, updateMessage); // this will run after every 1 seconds
// }, 1000);