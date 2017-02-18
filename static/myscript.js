// This script links to trip_detail.html
var map;
var uniqueId = 0;
var markers = [];

//JQuery to update messages\\


$(document).ready(function() {

  var socket = io.connect('127.0.0.1:5000');

  socket.on('connect', function () {
    console.log("connected and about to join room %s", tripCode);
    console.log(socket);
    socket.emit('join', tripCode);
  });

  // socket.on('connect', function () {
  //   console.log('User has connected!'); });

  //   // socket.send('User has connected!'); });

  socket.on('message', function(msg) {
    $("#messages").append('<li>' + msg + '</li>');
    console.log('Received message');
  });

  $('#sendbutton').on('click', function() {
    socket.emit('json', { "msg": $("#mytext").val(), "room": tripCode});
    $("#mytext").val(''); }); });




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

function init() {
  var tables = document.getElementsByClassName("editabletable");
  var i;
  for (i = 0; i < tables.length; i++)
  {
      makeTableEditable(tables[i]);
  }
}

function makeTableEditable(table) {
  var rows = table.rows;
  var r;
  for (r = 0; r < rows.length; r++) {
      var cols = rows[r].cells;
      var c;
      for (c = 0; c < cols.length; c++) {
          var cell = cols[c];
          var listener = makeEditListener(table, r, c);
          cell.addEventListener("input", listener, false);
      }
  }
}

function makeEditListener(table, row, col) {
    return function(event) {
        var cell = getCellElement(table, row, col);
        var text = cell.innerHTML.replace(/<br>$/, '');
        var items = split(text);

        if (items.length === 1) {
            // Text is a single element, so do nothing.
            // Without this each keypress resets the focus.
            return;
        }

        var i;
        var r = row;
        var c = col;
        for (i = 0; i < items.length && r < table.rows.length; i++) {
            cell = getCellElement(table, r, c);
            cell.innerHTML = items[i]; // doesn't escape HTML
            c++;
            if (c === table.rows[r].cells.length) {
                r++;
                c = 0;
            }
        }
        cell.focus();
    };
}

function getCellElement(table, row, col) {
    // assume each cell contains a div with the text
    return table.rows[row].cells[col].firstChild;
}

function split(str) {
    // use comma and whitespace as delimiters
    return str.split(/,|\s|<br>/);
}

init();


// The function initializes the map with origin on San Francisco
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.774, lng: -122.431},
    zoom: 10,
    mapTypeId: 'terrain'
   
  });

  $.get('/add_marker.json/'+tripCode, showMarkers);

  // Geocoding method geocodes one location per request when submit button
  // is pushed. 
  var geocoder = new google.maps.Geocoder();
  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map); });
  
  // calls in function placeMarkerAndPanTo on double click action
  map.addListener('dblclick', function(evt) {
    placeMarkerAndPanTo(evt.latLng); });
}

// Function that check to see if there are any markers. IIFE used to make sure 
//that marker object is not overwritten (line starting with '(function' )
function showMarkers(data) {
  // console.log(data);
  if (data) {
    for (var key in data) {
      (function () {
        var myLatLng = {lat: data[key].lat, lng: data[key].lng};
        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          dragable: true});
        map.panTo(myLatLng);
        marker.id = uniqueId;
        marker.description = data[key].description;
        uniqueId ++;
        markers.push(marker);
        google.maps.event.addListener(marker, "rightclick", function (event) { showMarkerWindow(marker);});
      }());
    }
  }
}

// Creates info window for each marker with option to add description
function showMarkerWindow(marker) {
  var content = 'Latitude: ' + marker.position.lat() + '<br />Longitude: ' + marker.position.lng();
      content += "<br />Description:" + marker.description;
      content += "<br /><input type=text id='markdesc' name = 'markerdescription'>";
      content += "<input type='button' value='Update' onclick = 'addDescription(" + marker.id + ");' value = 'addDescription' />";
      content += "<br /><input type = 'button' value = 'Delete Marker' onclick = 'deleteMarker(" + marker.id + ")'; value='deleteMarker'/>";
      var infoWindow = new google.maps.InfoWindow({content: content});
      infoWindow.open(map, marker);
}

// Creates new marker and pushes marker to the markers array, pans map to
// the new marker
function placeMarkerAndPanTo(latLng) {
  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
    dragable: true});
  map.panTo(latLng);
  marker.id = uniqueId;
  uniqueId ++;
  markers.push(marker);

  // console.log(marker.position.lat());
  // This pops up a window with a marker description and option to delete
  // marker, calls function 'deleteMarker'
  google.maps.event.addListener(marker, "rightclick", function (event) { showMarkerWindow(marker); });
}


// Deletes markers
var deleteMarker = function (id) {
  for (var i = 0; i < markers.length; i++) {
    if (markers[i].id == id) {
      markers[i].setMap(null);
      markers.splice(i, 1);
      return;
    }
  }
};
       
// Adds description to marker
var addDescription = function(id) {
  for (var i = 0; i < markers.length; i++) {
    if (markers[i].id == id) {
      markers[i].description = document.getElementById('markdesc').value;
      return;
    }
  }
};
      
//Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    console.log(markers[i]);
    markers[i].setMap(map);
  }
}

// The function geocodes for a specific address typed-in in the input,
// centers the map at the address and creates marker
function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      // The 4 lines below place a marker when Geocode btn is clicked; removed
      // it to make it less confusing
      // var marker = new google.maps.Marker({
      //   map: resultsMap,
      //   position: results[0].geometry.location
      // });
      // console.log(marker.position.lng());
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

document.getElementById('submarker').addEventListener('click', function() {saveRoute(markers); } );

// Post data to flask
function saveRoute(markers) {
  event.preventDefault();

  var dataInput = {};
  console.log(markers);
  for (var i = 0; i < markers.length; i++) {
      dataInput[markers[i].id] = {
      "lat": markers[i].position.lat(),
      "lng": markers[i].position.lng(),
      "marker_id": markers[i].id,
      "marker_description": markers[i].description};
  }
  my_data = {"data": JSON.stringify(dataInput), "trip_code": tripCode};
  // console.log(my_data);
  $.post('/add_marker.json', my_data, function() {alert("You successfully logged this trip");});
}

