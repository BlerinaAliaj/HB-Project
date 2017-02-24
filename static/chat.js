// Script for socketIO real time messaging

$(document).ready(function() {

  var socket = io.connect('127.0.0.1:5000');

  socket.on('connect', function () {
    console.log("connected and about to join room %s", tripCode);
    console.log(socket);
    socket.emit('join', tripCode);
  });


socket.on('message', function(msg) {
  $("#messages").append('<li>' + msg + '</li>');
  console.log('Received message');
});

$('#sendbutton').on('click', function() {
  socket.emit('json', { "msg": $("#mytext").val(), "room": tripCode});
  $("#mytext").val(''); }); });

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