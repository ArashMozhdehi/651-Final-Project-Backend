var connected = 0;
var disconnected = 0;
var mqtt;
var reconnectTimeout = 2000;
var map;
var infoWindow = null;
var infoWindow1 = null;
var infoWindow2 = null;
var infoWindow3 = null;
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

function initialize() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: { lat: 51.035999, lng: -114.066666},
    zoom: 11.3,
    styles: styles["hide"]
  });
  map.setOptions({ styles: styles["hide"] });
  const bikeLayer = new google.maps.BicyclingLayer();
  // bikeLayer.setMap(map);
  MQTTconnect();
}
function onConnectionLost() {
  console.log("connection lost");
  if(disconnected==1){

  }
  else{
    setTimeout(MQTTconnect, reconnectTimeout);
  }
  connected = 0;
}

function onFailure(message) {
  console.log("connection failed");
  setTimeout(MQTTconnect, reconnectTimeout);
}

function onMessageArrived(r_message) {
  out_msg = r_message.payloadString;
  // alert("Message:" + out_msg)
  showlocation(out_msg);
  console.log(out_msg);
  // document.getElementById("messages").innerHTML = out_msg;
}

function onConnected(recon, url) {
  sub_topics();
  console.log(" in onConnected " + reconn);
}

function onConnect() {
  connected = 1;
  sub_topics();
  console.log("on Connect " + connected);
}

function disconnect() {
  if(connected==1){
    disconnected = 1;
    mqtt.disconnect();
    connected = 1;
  }
}

function MQTTconnect() {
  disconnected = 0;
  var s = "test.mosquitto.org";
  var p = "8081"
  if (p != "") {
    console.log("ports");
    port = parseInt(p);
    console.log("port" + port);
  }
  if (s != "") {
    host = s;
    console.log("host");
  }
  console.log("connecting to " + host + " " + port);
  var x = Math.floor(Math.random() * 10000);
  var cname = "orderform-" + x;
  mqtt = new Paho.MQTT.Client(host, port, cname);
  var options = {
    timeout: 4000,
    onSuccess: onConnect,
    onFailure: onFailure,
    useSSL:true
  };

  mqtt.onConnectionLost = onConnectionLost;
  mqtt.onMessageArrived = onMessageArrived;

  mqtt.connect(options);
  return false;
}

function sub_topics() {
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
  // let token = params.token;
  // let username = params.username;
  let token = document.getElementById('token').value
  let username = document.getElementById('username').value
  if (connected == 0) {
    out_msg = "Not connected so can't subscribe"
    console.log(out_msg);
    return false;
  }
  // var stopic = "bike_assistant/amozhdehi/1cd7ca60dbdce54295c67f2ceb8ae30c";
  var stopic = "bike_assistant/" + username + "/" + token;
  // alert(stopic);
  console.log("Subscribing to topic =" + stopic);
  mqtt.subscribe(stopic);
  return false;
}

function resetInfoWindows(){
  try {
    if(infowindow!=null)
      infowindow.close();
    } catch {}
  try {
    if(infowindow1!=null)
      infowindow1.close();
    } catch {}
  try {
    if(infowindow2!=null)
      infowindow2.close();
    } catch {}
  try {
    if(infowindow3!=null)
      infowindow3.close();
    } catch {}
}

function showlocation(locationText) {
  try {
    var json = JSON.parse(locationText);
    let cur_lat = parseFloat(json.cur_lat);
    let cur_lng = parseFloat(json.cur_lng);
    let src_lat = parseFloat(json.src_lat);
    let src_lng = parseFloat(json.src_lng);
    let dst_lat = parseFloat(json.dst_lat);
    let dst_lng = parseFloat(json.dst_lng);
    let speed = parseFloat(json.speed);
    map = new google.maps.Map(document.getElementById('map-canvas'), {
      center: { lat: (cur_lat+dst_lat)/2, lng: (dst_lng+cur_lng)/2},
      zoom: 13.2,
      styles: styles["hide"]
    });

    const currMarker = {
      // path: "M240.839587,233.308318 C229.423358,233.308318 220.133174,223.984445 220.133174,212.524128 C220.133174,203.95543 225.327505,196.584636 232.719991,193.408318 L238.47678,214.282985 C238.739982,215.229969 239.594486,215.850033 240.52711,215.850033 C240.715798,215.850033 240.90689,215.824699 241.09678,215.772826 C242.23011,215.457969 242.894725,214.280572 242.579844,213.142985 L236.788202,192.144065 C238.099404,191.882287 239.45267,191.739938 240.839587,191.739938 C252.257018,191.739938 261.546,201.063811 261.546,212.524128 C261.546,223.984445 252.257018,233.308318 240.839587,233.308318 L240.839587,233.308318 Z M200.602156,206.802414 C199.375083,205.996572 197.91245,205.52489 196.34045,205.52489 C196.261128,205.52489 196.185413,205.534541 196.106092,205.536953 L187.34111,179.946668 L225.216936,179.65835 L200.602156,206.802414 Z M159.963312,233.308318 C148.545881,233.308318 139.256899,223.984445 139.256899,212.524128 C139.256899,201.063811 148.545881,191.739938 159.963312,191.739938 C163.627706,191.739938 167.067358,192.709842 170.057523,194.393906 L158.486257,212.375747 C158.066817,213.027176 158.031963,213.855938 158.396119,214.539938 C158.760275,215.225144 159.46455,215.658223 160.23733,215.670287 L180.353642,216.014096 C178.692706,225.814477 170.19333,233.308318 159.963312,233.308318 L159.963312,233.308318 Z M180.630064,211.744826 L164.139688,211.464953 L173.535633,196.864509 C177.713211,200.517334 180.410128,205.813207 180.630064,211.744826 L180.630064,211.744826 Z M196.34045,216.935747 C195.562862,216.935747 194.850174,216.676382 194.264881,216.251747 C193.370716,215.602731 192.78422,214.554414 192.78422,213.36616 C192.78422,212.865525 192.88878,212.390223 193.075064,211.95835 C193.195248,211.678477 193.358697,211.42635 193.542578,211.189906 C194.192771,210.347874 195.198706,209.796572 196.34045,209.796572 C196.804358,209.796572 197.245431,209.89308 197.651651,210.055938 C197.652853,210.055938 197.654055,210.057144 197.655257,210.057144 C198.965257,210.584318 199.895477,211.865461 199.895477,213.36616 C199.895477,213.583303 199.869037,213.793207 199.830578,213.999493 C199.531321,215.664255 198.084312,216.935747 196.34045,216.935747 L196.34045,216.935747 Z M183.389477,181.548699 L192.046294,206.821715 C190.321661,207.965334 189.075358,209.774858 188.671541,211.88235 L184.908596,211.818414 C184.701881,204.352318 181.230982,197.689652 175.872,193.230985 L183.389477,181.548699 Z M240.839587,187.467049 C239.060872,187.467049 237.32422,187.658858 235.650064,188.014731 L229.769486,166.699747 C240.047578,165.686414 243.471606,166.703366 244.604936,167.439239 C245.250321,167.859049 245.711826,168.797588 245.869266,170.017207 C246.098817,171.795366 245.606064,173.421525 245.162587,173.911303 C244.276835,174.888445 241.969312,175.456636 239.280807,175.350477 C238.090991,175.317906 237.116303,176.223874 237.071835,177.402477 C237.026165,178.582287 237.943165,179.573906 239.117358,179.619747 C241.510211,179.712636 245.88489,179.465334 248.312596,176.786033 C249.737972,175.210541 250.453064,172.269461 250.088908,169.465906 C249.765615,166.963938 248.638294,164.971049 246.918468,163.852763 C243.810523,161.834541 237.417963,161.476255 226.802156,162.72362 C226.185615,162.796001 225.631569,163.136191 225.284239,163.652509 C224.936908,164.170033 224.83355,164.814223 224.998202,165.414985 L227.743193,175.36616 L185.882083,175.684636 L184.00722,170.212636 L192.641202,170.212636 C193.816596,170.212636 194.769651,169.256001 194.769651,168.076191 C194.769651,166.896382 193.816596,165.939747 192.641202,165.939747 L173.486358,165.939747 C172.310963,165.939747 171.357908,166.896382 171.357908,168.076191 C171.357908,169.256001 172.310963,170.212636 173.486358,170.212636 L179.506349,170.212636 L181.644413,176.454287 C181.579514,176.52908 181.508606,176.597842 181.453321,176.682287 L172.372257,190.796572 C168.713872,188.683049 164.478606,187.467049 159.963312,187.467049 C146.198697,187.467049 135,198.707811 135,212.524128 C135,226.340445 146.198697,237.581207 159.963312,237.581207 C172.522486,237.581207 182.939991,228.221144 184.669431,216.087684 L189.050119,216.162477 C190.175037,219.107176 193.014972,221.20743 196.34045,221.20743 C200.647826,221.20743 204.152376,217.689715 204.152376,213.36616 C204.152376,212.181525 203.880761,211.060826 203.410844,210.053525 L229.404128,181.387049 L231.577046,189.263303 C222.386615,192.964382 215.876275,201.992699 215.876275,212.524128 C215.876275,226.340445 227.074972,237.581207 240.839587,237.581207 C254.604202,237.581207 265.802899,226.340445 265.802899,212.524128 C265.802899,198.707811 254.604202,187.467049 240.839587,187.467049 L240.839587,187.467049 Z",
      //
      path: "M512.509 192.001c-16.373-.064-32.03 2.955-46.436 8.495l-77.68-125.153A24 24 0 0 0 368.001 64h-64c-8.837 0-16 7.163-16 16v16c0 8.837 7.163 16 16 16h50.649l14.896 24H256.002v-16c0-8.837-7.163-16-16-16h-87.459c-13.441 0-24.777 10.999-24.536 24.437.232 13.044 10.876 23.563 23.995 23.563h48.726l-29.417 47.52c-13.433-4.83-27.904-7.483-42.992-7.52C58.094 191.83.412 249.012.002 319.236-.413 390.279 57.055 448 128.002 448c59.642 0 109.758-40.793 123.967-96h52.033a24 24 0 0 0 20.406-11.367L410.37 201.77l14.938 24.067c-25.455 23.448-41.385 57.081-41.307 94.437.145 68.833 57.899 127.051 126.729 127.719 70.606.685 128.181-55.803 129.255-125.996 1.086-70.941-56.526-129.72-127.476-129.996zM186.75 265.772c9.727 10.529 16.673 23.661 19.642 38.228h-43.306l23.664-38.228zM128.002 400c-44.112 0-80-35.888-80-80s35.888-80 80-80c5.869 0 11.586.653 17.099 1.859l-45.505 73.509C89.715 331.327 101.213 352 120.002 352h81.3c-12.37 28.225-40.562 48-73.3 48zm162.63-96h-35.624c-3.96-31.756-19.556-59.894-42.383-80.026L237.371 184h127.547l-74.286 120zm217.057 95.886c-41.036-2.165-74.049-35.692-75.627-76.755-.812-21.121 6.633-40.518 19.335-55.263l44.433 71.586c4.66 7.508 14.524 9.816 22.032 5.156l13.594-8.437c7.508-4.66 9.817-14.524 5.156-22.032l-44.468-71.643a79.901 79.901 0 0 1 19.858-2.497c44.112 0 80 35.888 80 80-.001 45.54-38.252 82.316-84.313 79.885z",
      fillColor: "yellow",
      fillOpacity: 1,
      strokeWeight: 1,
      rotation: 0,
      scale: .10
    };

    const fMarker = {
      path: "M32 62c0-17.1 16.3-25.2 17.8-39.7A18 18 0 1 0 14 20a18.1 18.1 0 0 0 .2 2.2C15.7 36.8 32 44.9 32 62z",
      fillColor: "blue",
      fillOpacity: 1,
      strokeWeight: 1,
      rotation: 0,
      scale: 1,
      anchor: new google.maps.Point(40, 40),
    };

    const fMarker2 = {
      url: '../images/icons8-google-maps-96.png',
      fillOpacity: 1,
      strokeWeight: 2,
      strokeColor:"black",
      scaledSize: new google.maps.Size(60, 60),
    };

    const tMarker = {
      url: '../images/icons8-flag-filled-64.png',
      // path: 'M 0,0 -1,-2 V -43 H 1 V -2 z M 1,-40 H 30 V -20 H 1 z',
      fillOpacity: 1,
      strokeWeight: 2,
      strokeColor:"black",
      anchor: new google.maps.Point(0, 40),
      scaledSize: new google.maps.Size(40, 40),
      // scaledSize: new google.maps.Size(60, 60),
    };

    const cMarker = {
      url: '../images/bike_location.png',
      fillOpacity: 1,
      scaledSize: new google.maps.Size(40, 50),
    };

    fromMarker = null;
    toMarker = null;
    curMarker = null;

    fromMarker = new google.maps.Marker({
      map: map,
      position: { lat: src_lat, lng: src_lng},
      animation: google.maps.Animation.DROP,
      // icon:fMarker2,
    });

    toMarker = new google.maps.Marker({
      map: map,
      position: { lat: dst_lat, lng: dst_lng },
      animation: google.maps.Animation.BOUNCE,
      icon: tMarker,
    });

    curMarker = new google.maps.Marker({
      map: map,
      position: { lat: cur_lat, lng: cur_lng },
      animation: google.maps.Animation.BOUNCE,
      icon:cMarker
    });

    google.maps.event.addListener(curMarker, 'click', function() {
      resetInfoWindows();
      infowindow1.open(map, curMarker);
    });
        infowindow1 = new google.maps.InfoWindow({
        content: "<b>Current Location</b><br><br><span>Here is the current location of the user.</span><br><br><b>Current Speed: </b>" + speed
    });

    google.maps.event.addListener(fromMarker, 'click', function() {
      resetInfoWindows();
      infowindow2.open(map, fromMarker);
    });
        infowindow2 = new google.maps.InfoWindow({
        content: "<b>Starting Point</b><br><br><span>This is where the user started.</span>"
    });


    google.maps.event.addListener(toMarker, 'click', function() {
      resetInfoWindows();
      infowindow3.open(map, toMarker);
    });
        infowindow3 = new google.maps.InfoWindow({
        content: "<b>Destination</b><br><br><span>This location is the user's destination.</span>"
    });

    var remaining_distance = 0;
    var remaining_duration = 0;

    var ds0 = new google.maps.DirectionsService();
    ds0.route({
      origin: curMarker.getPosition(),
      destination: toMarker.getPosition(),
      travelMode: google.maps.TravelMode.BICYCLING,
      unitSystem: google.maps.UnitSystem.METRIC
    }, function (result, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        for (let i = 0; i < result.routes[0].legs.length; i++) {
          remaining_distance += result.routes[0].legs[i].distance.value;
          remaining_duration += result.routes[0].legs[i].duration.value;
        }
      }
    });


    var ds = new google.maps.DirectionsService();
    var routePath = null;
    var path = null;
      ds.route({
        origin: fromMarker.getPosition(),
        destination: toMarker.getPosition(),
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
          console.log(result);

          result.routes[0].legs.forEach(function (leg) {
            leg.steps.forEach(function (step) {
              fullPath = fullPath.concat(step.path);
              routePath = new google.maps.Polyline({
                map: map,
                path: step.path,
                strokeColor: "red",
                strokeWeight: 7
              });
              google.maps.event.addListener(routePath, 'click', function (e) {
                resetInfoWindows();
                try{
                  infoWindow.close();
                }
                catch{}
                infoWindow = new google.maps.InfoWindow();
                 var location = e.latLng;
                 // alert(location);
                 console.log(location);
                 infoWindow.setContent('<b>Trip information</b><br><br><b>Total distance:</b> ' + distance/1000
                 + ' km<br><b>Estimated total duration:</b> '
                 + (duration/60).toFixed(0) + ' mins<br><b>Remanining distance:</b> ' + remaining_distance/1000 +
                  ' km<br><b>Estimated remaining duration:</b> ' + (remaining_duration / 60).toFixed(0) +' mins');
                 infoWindow.setPosition(location);
                 infoWindow.open(map);
              });
            });
          });
        }
      });
  }
  catch (err) {
    alert(err)
  }
}
