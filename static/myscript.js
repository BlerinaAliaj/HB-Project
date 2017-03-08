// This script links to trip_detail.html and updates/loads maps, markers, routes
// The interactive tables are inputed here

// *****************************************************************************
// JS for Google Maps
// The function initializes the map with origin on San Francisco

var map;
var uniqueId = 0;
var markers = [];
var timeout;
var chart;
var elSvc;
var path = new Array();

function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.733493, lng: -119.594947},
    zoom: 15,
    mapTypeId: 'terrain'
   
  });

  $.get('/add_marker.json/'+tripCode, showMarkers);

  // $.get('/add_alt_graph'+tripCode, function() { 

    // plottingComplete(data);

  // });

  map.data.addListener('click', function(mouseEvent) {
    var geometry = mouseEvent.feature.getGeometry();
    var feat_id = mouseEvent.feature.getProperty("id");
    var box = mouseEvent.feature.getProperty('window');

    var points = [];

    if (geometry.getType() === 'MultiLineString') {
        geometry.getArray.forEach(function(lineString) {
          points.push.apply(points, lineString.getArray());
        });
    } else {
        points.push.apply(points, geometry.getArray());
    }

    // var route_info = {"route_id": feat_id,
    //               "bounding_box": box };

    // $.post('/add_alt_graph'+tripCode, route_info, function() {alert('We added this graph');});


    plottingComplete(points);
    
        $("#second-image").slideUp();
        $("#elevation_chart").attr("class", "col-xs-4");

  });

  chart = new google.visualization.ColumnChart(document.getElementById('elevation_chart'));

  // Creates an elevation service

  elSvc = new google.maps.ElevationService();

  // Geocoding method geocodes one location per request when submit button
  // is pushed. 
  var geocoder = new google.maps.Geocoder();
  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map); });
  
  // calls in function placeMarkerAndPanTo on double click action
  map.addListener('dblclick', function(evt) {
    placeMarkerAndPanTo(evt.latLng);
     });

  map.addListener('bounds_changed', function () {
    clearTimeout(timeout);
    timeout = setTimeout(queryGISDatabase.bind(null, map), 1000);
  });
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
        // This is where I set up marker paths
        path.push(myLatLng);
        google.maps.event.addListener(marker, "rightclick", function (event) { showMarkerWindow(marker);});
      }());
    }
  }
  // console.log(markers[0].position.lat());
}

// Creates info window for each marker with option to add description
function showMarkerWindow(marker) {

  var markerDesc = marker.description;
  if ( typeof(markerDesc) == "undefined")  {
    markdesc = "No description";
  }

  var content = 'Latitude: ' + marker.position.lat() + '<br />Longitude: ' + marker.position.lng();
      content += "<br />Description: " + markerDesc;
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
  path.push(latLng);

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
      path.splice(i, 1);
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

      queryGISDatabase(resultsMap);

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

document.getElementById('submarker').addEventListener('click', function(event) {
  saveRoute(markers);
  });

// Post data to flask
function saveRoute(markers) {
  event.preventDefault();
  plottingComplete();

  var dataInput = {};
  // console.log(markers);
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


function plottingComplete(path) {
  // console.log('We are here');
  // console.log(path);
  // var pathOptions = {
  //   path: path,
  //   strokeColor: '#0000CC',
  //   opacity: 0.4,
  //   map: map
  // };

  // polyline = new google.maps.Polyline(pathOptions);

  var pathRequest = {
    'path': path,
    'samples': 256
  };
  elSvc.getElevationAlongPath(pathRequest, plotElevation);
}


function plotElevation(results, status){
  if (status == google.maps.ElevationStatus.OK) {
    elevation = results;

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Sample');
    data.addColumn('number', 'Elevation');
    for (var i = 0; i < results.length; i++) {
      data.addRow(['', elevation[i].elevation]);
    }
    // document.getElementById('elevation_chart').style.display = 'block';
    chart.draw(data, {
      legend: 'none',
      titleY: 'Elevation (m)'
    });
  }
}

function queryGISDatabase(resultsMap) {

  // get values for viewport
  var latNE = resultsMap.getBounds().getNorthEast().lat();
  var lngNE = resultsMap.getBounds().getNorthEast().lng();
  var latSW = resultsMap.getBounds().getSouthWest().lat();
  var lngSW = resultsMap.getBounds().getSouthWest().lng();

  // console.log(latNE, lngNE, latSW, lngSW);

  var myViewPort = {'latNE': latNE, 'lngNE': lngNE, 'latSW': latSW, 'lngSW': lngSW };

  // Push viewport data to server route that will filter database tables 
  // based on viewport
  $.get("/query_osm.json", myViewPort, function(gisDataJSON){
    var li = $("#trailDesc");

    map.data.forEach(function (feature) {
      li.empty();
      map.data.remove(feature);
    });

    var gisData = JSON.parse(gisDataJSON);
    for (var key in gisData) {
      // console.log("Adding: %s", JSON.stringify(gisData[key]));
      var featureJSON = gisData[key];
      // console.log(featureJSON.geometry.coordinates);
      var featureID = featureJSON.properties.id;
      var featureName = featureJSON.properties.name;
      // console.log(featureName);

      var mapFeature = map.data.addGeoJson(featureJSON)[0];
      // console.log(mapFeature);
      var featureColor = '#' + Math.abs(featureID).toString(16).substr(0,6);
      li.append("<li style='color:"+featureColor+";'>" + featureName + '</li>');


      map.data.overrideStyle(mapFeature, {strokeColor: featureColor, clickable: true});
      // mapFeature.onclick()
    }
    // alert("Yay");
  });
}

$(document).ready(function () {
  var statsDiv = $('#stats');
  var todoDiv = $('#todolist');
      $(".toggle-list").click(function (event) {
        if (statsDiv.is(":visible")) {
          statsDiv.slideUp(400, function() {
            todoDiv.slideDown();
          });

        } else {
          todoDiv.slideUp(400, function() {
            statsDiv.slideDown();
          });
          event.preventDefault();
        }
        
      });
    });

