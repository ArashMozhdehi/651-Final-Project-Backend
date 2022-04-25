var historics_array;
var events_array;
var bikeparkings_array;
var parks_array;
var historics_marker_array = [];
var events_marker_array = [];
var bikeparkings_marker_array = [];
var parks_marker_array = [];
var map;

var cur_lat;
var cur_lng;
var cur_marker;
var parks_marker_cluster;
var bikeparkings_marker_cluster;
var events_marker_cluster;
var historics_marker_cluster;
var open_info_window=null;

var parks_checked = true;
var bikeparkings_checked = true;
var events_checked = true;
var historics_checked = true;

var path = null;
var routePath = null;
var routePaths = [];

function show_path(fromPosition, toPosition) {
  if (routePath != null) {
      path.setMap(null);
      routePath.setMap(null);
      for (path in routePaths) {
        routePaths[path].setMap(null);
      }
  }
  var ds = new google.maps.DirectionsService();
  routePath = null;
  path = null;
  routePaths = [];
    ds.route({
      origin: fromPosition,
      destination: toPosition,
      travelMode: google.maps.TravelMode.BICYCLING,
      unitSystem: google.maps.UnitSystem.METRIC
    }, function (result, status) {
      if (status == google.maps.DirectionsStatus.OK) {

         path = new google.maps.Polyline({
          map: map,
          path: result.routes[0].overview_path
        });

        var fullPath = [];
        var distance = 0;
        var duration = 0;
        for (let i = 0; i < result.routes[0].legs.length; i++) {
          distance += result.routes[0].legs[i].distance.value;
          duration += result.routes[0].legs[i].duration.value;
        }
        // alert("distnace:" + distance +", duration: " + duration);
        // console.log(result);

        result.routes[0].legs.forEach(function (leg) {
          leg.steps.forEach(function (step) {
            fullPath = fullPath.concat(step.path);
            routePath = new google.maps.Polyline({
              map: map,
              path: step.path,
              strokeColor: "red",
              strokeWeight: 7
            });
            routePaths.push(routePath);
            google.maps.event.addListener(routePath, 'click', function (e) {
              try{
                open_info_window.close();
              }
              catch{}
              var infoWindow5 = new google.maps.InfoWindow();
               var location = e.latLng;
               // alert(location);
               // console.log(location);
               infoWindow5.setContent('<b>Trip information</b><br><br><b>Total distance:</b> ' + distance/1000
               + ' km<br><b>Estimated total duration:</b> '
               + (duration/60).toFixed(0) + ' mins');
               infoWindow5.setPosition(location);
               infoWindow5.open(map);
               open_info_window = infoWindow5;
            });
          });

        });
      }
    });
}

function initialize() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: { lat: 51.035999, lng: -114.066666},
    zoom: 10.9
  });
  map.setOptions({ styles: styles["hide"] });

  const bikeLayer = new google.maps.BicyclingLayer();
  overlayControls(map);
  getlocation();
  fetchBikeParkings();
  fetchParks();
  fetchEvents();
  fetchHistorics();
}

function overlayControls (map) {
  const controlDiv = document.createElement("div");
  const controlUI = document.createElement("div");
  controlUI.style.backgroundColor = "#240259";
  controlUI.style.border = "2px solid #240259";
  controlUI.style.borderRadius = "3px";
  controlUI.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlUI.style.cursor = "pointer";
  controlUI.style.marginTop = "8px";
  controlUI.style.marginBottom = "22px";
  controlUI.style.textAlign = "center";
  controlUI.title = "Click to move back to the previous page.";
  controlDiv.appendChild(controlUI);
  const controlText = document.createElement("div");
  controlText.style.color = "rgb(255,255,255)";
  controlText.style.fontFamily = "Roboto,Arial,sans-serif";
  controlText.style.fontSize = "16px";
  controlText.style.lineHeight = "38px";
  controlText.style.paddingLeft = "5px";
  controlText.style.paddingRight = "5px";
  controlText.innerHTML = "Move Back";
  controlUI.appendChild(controlText);
  controlUI.addEventListener("click", () => {
    window.location.href="/dashboard";
  });
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv);

  var checkOptions1 = {
     gmap: map,
     title: "Throught this you can select/unselect Bike Parks in the City of Calgary.",
     id: "parksCheck",
     label: "Bike Parks",
     action: function() {
       // var parks_marker_array
       if(parks_checked) {
          for(marker in parks_marker_array) {
            parks_marker_array[marker].setVisible(false);
          }
          parks_checked = false;
       }
       else {
         for(marker in parks_marker_array) {
           parks_marker_array[marker].setVisible(true);
         }
         parks_checked = true;
       }
       parks_marker_cluster.repaint();
     }
  }
  var check1 = new checkBox(checkOptions1);
  var checkOptions2 = {
     gmap: map,
     title: "Throught this you can select/unselect Currecnt Events in the City of Calgary.",
     id: "eventsCheck",
     label: "City Events",
     action: function() {
       // var events_marker_array = [];
       if(events_checked) {
          for(marker in events_marker_array) {
            events_marker_array[marker].setVisible(false);
          }
          events_checked = false;
       }
       else {
         for(marker in events_marker_array) {
           events_marker_array[marker].setVisible(true);
         }
         events_checked = true;
       }
       events_marker_cluster.repaint();
     }
  }
  var check2 = new checkBox(checkOptions2);
  var checkOptions3 = {
     gmap: map,
     title: "Throught this you can select/unselect Parking Losts for Bikes in the City of Calgary.",
     id: "parkingsCheck",
     label: "Bike Parkings",
     action: function() {
       // var bikeparkings_marker_array = [];
       if(bikeparkings_checked) {
          for(marker in bikeparkings_marker_array) {
            bikeparkings_marker_array[marker].setVisible(false);
          }
          bikeparkings_checked = false;
       }
       else {
         for(marker in bikeparkings_marker_array) {
           bikeparkings_marker_array[marker].setVisible(true);
         }
         bikeparkings_checked = true;
       }
       bikeparkings_marker_cluster.repaint();
     }
  }
  var check3 = new checkBox(checkOptions3);
  var checkOptions4 = {
     gmap: map,
     title: "Throught this you can select/unselect Historical Sites Bikes in the City of Calgary.",
     id: "historicCheck",
     label: "Historical Sites",
     action: function(){
       // var historics_marker_array = [];
       if(historics_checked) {
          for(marker in historics_marker_array) {
            historics_marker_array[marker].setVisible(false);
          }
          historics_checked = false;
       }
       else {
         for(marker in historics_marker_array) {
           historics_marker_array[marker].setVisible(true);
         }
         historics_checked = true;
       }
       historics_marker_cluster.repaint();
     }
  }
  var check4 = new checkBox(checkOptions4);
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(check1);
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(check2);
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(check3);
  map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(check4);
}


  function optionDiv(options){
    var control = document.createElement('DIV');
    control.className = "dropDownItemDiv";
    control.title = options.title;
    control.id = options.id;
    control.innerHTML = options.name;
    control.ariaChecked = true;
    google.maps.event.addDomListener(control,'click',options.action);
    return control;
   }

   function checkBox(options){
    //first make the outer container
    var container = document.createElement('DIV');
      container.className = "checkboxContainer";
      container.title = options.title;
      container.setAttribute("aria-checked", true);

    var span = document.createElement('SPAN');
    span.role = "checkbox";
    // span.ariaChecked = true;
    span.className = "checkboxSpan";
    span.setAttribute("aria-checked", true);


    // span.checked = true;

    var bDiv = document.createElement('DIV');
      bDiv.className = "blankDiv";
      bDiv.id = options.id;
      bDiv.setAttribute("aria-checked", true);

      var image = document.createElement('IMG');
      image.className = "blankImg";
      image.src = "http://maps.gstatic.com/mapfiles/mv/imgs8.png";

      var label = document.createElement('LABEL');
      label.className = "checkboxLabel";
      label.innerHTML = options.label;
      label.setAttribute("aria-checked", true);
      // document.getElementById(bDiv.id).setAttribute("aria-checked", true);
      // document.getElementById(span.id).setAttribute("aria-checked", true);



      bDiv.appendChild(image);
      span.appendChild(bDiv);
      container.appendChild(span);
      container.appendChild(label);

      google.maps.event.addDomListener(container,'click',function(){
        (document.getElementById(bDiv.id).style.display == 'block') ? document.getElementById(bDiv.id).style.display = 'none' : document.getElementById(bDiv.id).style.display = 'block';
        options.action();
      })
      return container;
   }
   function separator(){
      var sep = document.createElement('DIV');
      sep.className = "separatorDiv";
      return sep;
   }

   function dropDownOptionsDiv(options){
    //alert(options.items[1]);
      var container = document.createElement('DIV');
      container.className = "dropDownOptionsDiv";
      container.id = options.id;


      for(i=0; i<options.items.length; i++){
        //alert(options.items[i]);
        container.appendChild(options.items[i]);
      }

      //for(item in options.items){
        //container.appendChild(item);
        //alert(item);
      //}
  return container;
    }

   function dropDownControl(options){
      var container = document.createElement('DIV');
      container.className = 'container';

      var control = document.createElement('DIV');
      control.className = 'dropDownControl';
      control.innerHTML = options.name;
      control.id = options.name;
      var arrow = document.createElement('IMG');
      arrow.src = "http://maps.gstatic.com/mapfiles/arrow-down.png";
      arrow.className = 'dropDownArrow';
      control.appendChild(arrow);
      container.appendChild(control);
      container.appendChild(options.dropDown);

      options.gmap.controls[options.position].push(container);
      google.maps.event.addDomListener(container,'click',function(){
      (document.getElementById('myddOptsDiv').style.display == 'block') ? document.getElementById('myddOptsDiv').style.display = 'none' : document.getElementById('myddOptsDiv').style.display = 'block';
      setTimeout( function(){
        document.getElementById('myddOptsDiv').style.display = 'none';
      }, 1500);
      })
    }

   function buttonControl(options) {
       var control = document.createElement('DIV');
       control.innerHTML = options.name;
       control.className = 'button';
       control.index = 1;

       // Add the control to the map
       options.gmap.controls[options.position].push(control);

       // When the button is clicked pan to sydney
       google.maps.event.addDomListener(control, 'click', options.action);
       return control;
   }


   function fetchParks() {
     var url = 'https://data.calgary.ca/resource/jw79-78tx.json';
     fetch(url)
          .then(res => res.json())
              .then((out) => {
                parks_array = JSON.parse(JSON.stringify(out));
                toastr.success(parks_array.length + " Parks successfully loaded");
                for(park in parks_array) {
                  name = parks_array[park]['name'];
                  // alert(name);
                  longitude = parseFloat(parks_array[park]['longitude']);
                  latitude = parseFloat(parks_array[park]['latitude']);
                  general_info = parks_array[park]['general_info'];
                  const infoWindow = new google.maps.InfoWindow({
                    content: "",
                    disableAutoPan: true,
                  });
                  const cMarker = {
                    url: "https://img.icons8.com/external-nawicon-flat-nawicon/64/000000/external-park-location-nawicon-flat-nawicon.png",
                    fillOpacity: 1,
                    scaledSize: new google.maps.Size(50, 50),
                  };
                  // console.log("longitude: "+longitude);
                  // console.log("latitude: "+latitude);
                  // console.log("name: "+name);
                  // console.log("general_info: "+general_info);
                  var label = "<b>" + name + "</b><br><br><span><b>Information:</b> " + general_info + "</span>";
                  // var parks_checked = false;
                  const marker = new google.maps.Marker({
                    position: { lat: latitude, lng: longitude},
                    icon: cMarker,
                    map:map,
                    title:label,
                    // labal: {label},
                    visible:parks_checked,
                  });
                  // marker.setLabel(label);
                  marker.addListener("click", () => {
                    // alert(marker.getTitle());
                    show_path(cur_marker.getPosition(), marker.getPosition());
                    if(open_info_window != null) {
                      open_info_window.close()
                    }
                    infoWindow.setContent(marker.getTitle());
                    infoWindow.open(map, marker);
                    open_info_window = infoWindow;
                  });
                  parks_marker_array.push(marker);
                }
                // const markerCluster = new markerClusterer.MarkerClusterer({ parks_marker_array, map });
                parks_marker_cluster = new MarkerClusterer(map, parks_marker_array, {
                  ignoreHidden: true,
                  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
                });
                parks_marker_cluster.repaint();
                // console.log(parks[0]['general_info']);
              }).catch(err => console.error(err));
   }

   function fetchBikeParkings() {
     var url = 'https://data.calgary.ca/resource/fbvs-aj5g.json';
     fetch(url)
          .then(res => res.json())
              .then((out) => {
                bikeparkings_array = JSON.parse(JSON.stringify(out));
                toastr.success(bikeparkings_array.length + " Bike Parkades successfully loaded");
                for(bikepark in bikeparkings_array) {
                  name = bikeparkings_array[bikepark]['name'];
                  longitude = parseFloat(bikeparkings_array[bikepark]['longitude']);
                  latitude = parseFloat(bikeparkings_array[bikepark]['latitude']);
                  address = bikeparkings_array[bikepark]['address'];
                  const infoWindow1 = new google.maps.InfoWindow({
                    content: "",
                    disableAutoPan: true,
                  });
                  const bMarker = {
                    url: "https://img.icons8.com/pastel-glyph/64/000000/parking--v1.png",
                    fillOpacity: 1,
                    scaledSize: new google.maps.Size(50, 50),
                  };
                  // console.log("longitude: "+longitude);
                  // console.log("latitude: "+latitude);
                  // console.log("name: "+name);bikeparkings_array
                  // console.log("general_info: "+general_info);
                  var label = "<b>" + name + "</b><br><br><span><b>Address:</b> " + address + "</span>";
                  // var bikeparkings_checked = false;
                  const marker1 = new google.maps.Marker({
                    position: { lat: latitude, lng: longitude},
                    icon: bMarker,
                    // map:map,
                    title:label,
                    visible:bikeparkings_checked,
                  });
                  marker1.addListener("click", () => {
                    show_path(cur_marker.getPosition(), marker1.getPosition());
                    if(open_info_window != null) {
                      open_info_window.close()
                    }
                    infoWindow1.setContent(marker1.getTitle());
                    infoWindow1.open(map, marker1);
                    open_info_window = infoWindow1;
                  });
                  bikeparkings_marker_array.push(marker1);
                }
                // const markerCluster = new markerClusterer.MarkerClusterer({ parks_marker_array, map });
                bikeparkings_marker_cluster = new MarkerClusterer(map, bikeparkings_marker_array, {
                  ignoreHidden: true,
                  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
                });
                bikeparkings_marker_cluster.repaint();
                // console.log(parks[0]['general_info']);
              }).catch(err => console.error(err));
   }

   function fetchEvents() {
     var url = 'https://data.calgary.ca/resource/n625-9k5x.json';
     fetch(url)
          .then(res => res.json())
              .then((out) => {
                events_array = JSON.parse(JSON.stringify(out));
                var currentTime = new Date();
                const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                var month = monthNames[currentTime.getMonth()];
                var day = currentTime.getDate();
                var year = currentTime.getFullYear();
                var date = String(month) + " " + String(day) + " " + String(year);
                for(event_item in events_array) {
                  name = events_array[event_item]['title'];
                  longitude = parseFloat(events_array[event_item]['longitude']);
                  latitude = parseFloat(events_array[event_item]['latitude']);
                  address = events_array[event_item]['address'];
                  next_date_times = events_array[event_item]['next_date_times'];
                  event_type = events_array[event_item]['event_type'];
                  const infoWindow2 = new google.maps.InfoWindow({
                    content: "",
                    disableAutoPan: true,
                  });
                  const eMarker = {
                    url: "https://img.icons8.com/external-photo3ideastudio-flat-photo3ideastudio/64/000000/external-location-meeting-photo3ideastudio-flat-photo3ideastudio.png",
                    fillOpacity: 1,
                    scaledSize: new google.maps.Size(50, 50),
                  };
                  // var events_checked = false;
                  var label = "<b>" + name + "</b><br><br><span><b>Address:</b> " + address + "</span><br><span><b>Next Event:</b> " + next_date_times + "</span>";
                  const marker2 = new google.maps.Marker({
                    position: { lat: latitude, lng: longitude},
                    icon: eMarker,
                    title: label,
                    // map : map,
                    visible:events_checked,
                  });
                  marker2.addListener("click", () => {
                    show_path(cur_marker.getPosition(), marker2.getPosition());
                    if(open_info_window != null) {
                      open_info_window.close()
                    }
                    infoWindow2.setContent(marker2.getTitle());
                    infoWindow2.open(map, marker2);
                    open_info_window = infoWindow2;
                  });
                  if (next_date_times.includes(date)) {
                    // toastr.info(date);
                    // toastr.info(next_date_times);
                    events_marker_array.push(marker2);
                  }
                }
                // const markerCluster = new markerClusterer.MarkerClusterer({ parks_marker_array, map });
                toastr.success(events_marker_array.length + " Events for Today in the City successfully loaded");
                events_marker_cluster = new MarkerClusterer(map, events_marker_array, {
                  ignoreHidden: true,
                  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
                });
                events_marker_cluster.repaint();
                // console.log(parks[0]['general_info']);
              }).catch(err => console.error(err));
   }

   function fetchHistorics() {
     var url = 'https://data.calgary.ca/resource/99yf-6c5u.json';
     fetch(url)
          .then(res => res.json())
              .then((out) => {
                historics_array = JSON.parse(JSON.stringify(out));
                toastr.success(historics_array.length + " Historical Sites successfully loaded");
                for(site in historics_array) {
                  name = historics_array[site]['name'];
                  longitude = parseFloat(historics_array[site]['point']['coordinates'][0]);
                  latitude = parseFloat(historics_array[site]['point']['coordinates'][1]);
                  construction_yr = historics_array[site]['construction_yr'];
                  address = historics_array[site]['address'];
                  theme = historics_array[site]['master_plan_theme'];
                  builder = historics_array[site]['builder'];
                  development_era = historics_array[site]['development_era'];
                  // significance_summ = historics_array[site]['significance_summ'];
                  pic_url = historics_array[site]['pic_url'];
                  const infoWindow3 = new google.maps.InfoWindow({
                    content: "",
                    disableAutoPan: true,
                  });
                  const hMarker = {
                    url: "https://img.icons8.com/external-dreamcreateicons-outline-color-dreamcreateicons/64/000000/external-location-museum-dreamcreateicons-outline-color-dreamcreateicons.png",
                    fillOpacity: 1,
                    scaledSize: new google.maps.Size(40, 40),
                  };
                  // console.log("longitude: " + longitude);
                  // console.log("latitude: " + latitude);
                  // console.log("name: "+name);bikeparkings_array
                  // console.log("general_info: "+general_info);
                  var label = '<img style="display: block;margin-left: auto;margin-right: auto;width:300px;" src="'
                   + pic_url + '"/>' + "<br><br><b>" + name + "</b><br><br><span><b>Construction Year:</b> "
                   + construction_yr + "</span><br><span><b>Theme:</b> " + theme
                   + "</span><br><span><b>Builder:</b> " + builder
                   + "</span><br><span><b>Development Era:</b> " + development_era
                   "</span><br><span><b>Address:</b> " + address +
                    + "</span>";

                  // var historics_checked = false;

                  const marker3 = new google.maps.Marker({
                    position: { lat: latitude, lng: longitude},
                    icon: hMarker,
                    // map:map,
                    title:label,
                    visible:historics_checked,
                  });
                  marker3.addListener("click", () => {
                    show_path(cur_marker.getPosition(), marker3.getPosition());
                    if(open_info_window != null) {
                      open_info_window.close()
                    }
                    infoWindow3.setContent(marker3.getTitle());
                    infoWindow3.open(map, marker3);
                    open_info_window = infoWindow3;
                  });
                  historics_marker_array.push(marker3);
                }
                // const markerCluster = new markerClusterer.MarkerClusterer({ parks_marker_array, map });
                historics_marker_cluster = new MarkerClusterer(map, historics_marker_array, {
                  ignoreHidden: true,
                  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
                });
                historics_marker_cluster.repaint();
                // historics_marker_cluster.repaint();
                // console.log(parks[0]['general_info']);
              }).catch(err => console.error(err));
   }


   const styles = {
   default: [],
   hide: [
     {
       featureType: "poi.business",
       stylers: [{ visibility: "off" }],
     },
     {
       featureType: "poi.medical",
       stylers: [{ visibility: "off" }],
     },
     {
       featureType: "poi.school",
       stylers: [{ visibility: "off" }],
     },
     {
       featureType: "transit",
       elementType: "labels.icon",
       stylers: [{ visibility: "off" }],
     },
   ],
   };


 function getlocation() {
   try {
     if (navigator.geolocation) {
   		var options = {
   			enableHighAccuracy: true,
   			timeout: 5000,
   			maximumAge: 0
   		};
   		navigator.geolocation.getCurrentPosition(showPosition, null, options);
   	} else {
   		toastr.error("Sorry! your browser doesn't not support or allow getting your location.");
   	}
   } catch (e) {
     position.coords.latitude = 51.0745964050293;
     position.coords.longitude = -114.12068939209;
     showPosition(position);
   }
}

function showPosition(position) {
  try {
    cur_lat = position.coords.latitude;
    cur_lng = position.coords.longitude;
  } catch (e) {
    cur_lat = 51.0745964050293;
    cur_lng = -114.12068939209;
  }
  const infowindow = new google.maps.InfoWindow({
    content: "Your current location",
  });
  const cMarker = {
    url: "https://img.icons8.com/fluency/48/000000/user-location.png",
    fillOpacity: 1,
    scaledSize: new google.maps.Size(40, 40),
  };
  cur_marker = new google.maps.Marker({
    position: { lat: cur_lat, lng: cur_lng },
    map,
    title: "Your current location",
    animation: google.maps.Animation.BOUNCE,
    icon: cMarker,
  });
  cur_marker.addListener("click", () => {
    infowindow.open({
      anchor: cur_marker,
      map,
      shouldFocus: false,
    });
  });
}
