// *
// * Add multiple markers
// * 2013 - en.marnoto.com
// *

// necessary variables
var map;
var infoWindow;

// markersData variable stores the information necessary to each marker
//from the nyt warc, markersData = [{"lat": 42.0534, "lng": -88.054, "name": "secure-us.imrworldwide.com"}, {"lat": 39.018, "lng": -77.539, "name": "beacon.krxd.net"}, {"lat": 38.8943, "lng": -77.4311, "name": "static.dynamicyield.com"}, {"lat": 41.85, "lng": -87.65, "name": "kr.ixiaa.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "contextual.media.net"}, {"lat": 42.3626, "lng": -71.0843, "name": "cdn.optimizely.com"}, {"lat": 40.7357, "lng": -74.1724, "name": "cityroom.blogs.nytimes.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "qsearch.media.net"}, {"lat": 42.3626, "lng": -71.0843, "name": "typeface.nyt.com"}, {"lat": 37.751, "lng": -97.822, "name": "js-agent.newrelic.com"}, {"lat": 53.3478, "lng": -6.2597, "name": "connect.facebook.net"}, {"lat": 37.751, "lng": -97.822, "name": "cdn.krxd.net"}, {"lat": 42.3626, "lng": -71.0843, "name": "s1.nyt.com"}, {"lat": 37.751, "lng": -97.822, "name": "adadvisor.net"}, {"lat": 39.018, "lng": -77.539, "name": "3338050995.log.optimizely.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "b.scorecardresearch.com"}, {"lat": 38.9881, "lng": -77.4755, "name": "www.adadvisor.net"}, {"lat": 53.3331, "lng": -6.2489, "name": "core.fabrik.nytimes.com"}, {"lat": 40.7357, "lng": -74.1724, "name": "www.nytimes.com"}, {"lat": 40.7449, "lng": -73.9782, "name": "ckm-m.xp1.ru4.com"}, {"lat": 40.7357, "lng": -74.1724, "name": "static.nytimes.com"}, {"lat": 39.018, "lng": -77.539, "name": "s.tagsrvcs.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "sb.scorecardresearch.com"}, {"lat": 42.3646, "lng": -71.1028, "name": "www.w3.org"}, {"lat": 42.3626, "lng": -71.0843, "name": "a1.nyt.com"}, {"lat": 39.76, "lng": -98.5, "name": "googleads.g.doubleclick.net"}, {"lat": 29.4889, "lng": -98.3987, "name": "netpreserve.org"}, {"lat": 39.018, "lng": -77.539, "name": "meter-svc.nytimes.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "cdn3.optimizely.com"}, {"lat": 39.018, "lng": -77.539, "name": "sync.tidaltv.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "z.moatads.com"}, {"lat": 40.7357, "lng": -74.1724, "name": "mobile.nytimes.com"}, {"lat": 40.7449, "lng": -73.9782, "name": "p.rfihub.com"}, {"lat": 37.4192, "lng": -122.0574, "name": "www.googletagservices.com"}, {"lat": 39.018, "lng": -77.539, "name": "st.dynamicyield.com"}, {"lat": 37.4192, "lng": -122.0574, "name": "3951336.fls.doubleclick.net"}, {"lat": 47.6344, "lng": -122.3422, "name": "dc8xl0ndzn2cb.cloudfront.net"}, {"lat": 39.018, "lng": -77.539, "name": "pnytimes.chartbeat.net"}, {"lat": 42.3626, "lng": -71.0843, "name": "static01.nyt.com"}, {"lat": 41.8776, "lng": -87.6272, "name": "bam.nr-data.net"}, {"lat": 42.3626, "lng": -71.0843, "name": "a248.e.akamai.net"}, {"lat": 39.018, "lng": -77.539, "name": "tagx.nytimes.com"}, {"lat": 39.018, "lng": -77.539, "name": "et.nytimes.com"}, {"lat": 53, "lng": -8, "name": "www.facebook.com"}, {"lat": 39.018, "lng": -77.539, "name": "d.agkn.com"}, {"lat": 42.3626, "lng": -71.0843, "name": "as.casalemedia.com"}, {"lat": 39.018, "lng": -77.539, "name": "v4.moatads.com"}, {"lat": 37.4192, "lng": -122.0574, "name": "www.google-analytics.com"}, {"lat": 39.018, "lng": -77.539, "name": "new.webrecorder.io"}, {"lat": 39.018, "lng": -77.539, "name": "p2.keywee.co"}, {"lat": 39.018, "lng": -77.539, "name": "reading-list.api.nytimes.com"}];
var markersData = [{'lng': -122.0574, 'lat': 37.4192, 'domain': 'google.com'}, {'lng': -122.0074, 'lat': 37.4249, 'domain': 'yahoo.com'}, {'lng': -122.0574, 'lat': 37.4192, 'domain': 'youtube.com'}, {'lng': -122.1781, 'lat': 37.459, 'domain': 'facebook.com'}, {'lng': -78.1704, 'lat': 38.7163, 'domain': 'live.com'}, {'lng': -118.244, 'lat': 34.0544, 'domain': 'msn.com'}, {'lng': -122.3942, 'lat': 37.7898, 'domain': 'wikipedia.org'}, {'lng': -122.0574, 'lat': 37.4192, 'domain': 'blogger.com'}, {'lng': -118.4143, 'lat': 34.0995, 'domain': 'myspace.com'}, {'lng': 116.3883, 'lat': 39.9289, 'domain': 'baidu.com'}, {'lng': 137.3, 'lat': 34.85, 'domain': 'yahoo.co.jp'}, {'lng': -122.4156, 'lat': 37.7484, 'domain': 'wordpress.com'}, {'lng': -122.0574, 'lat': 37.4192, 'domain': 'google.co.in'}, {'lng': -122.0574, 'lat': 37.4192, 'domain': 'google.de'}, {'lng': 116.3883, 'lat': 39.9289, 'domain': 'qq.com'}, {'lng': -98.4936, 'lat': 29.4241, 'domain': 'microsoft.com'}, {'lng': '0', 'lat': '0', 'domain': 'rapidshare.com'}, {'lng': -118.2987, 'lat': 33.7866, 'domain': 'go.com'}, {'lng': 116.3883, 'lat': 39.9289, 'domain': 'sina.com.cn'}, {'lng': -122.0574, 'lat': 37.4192, 'domain': 'google.fr'}];
function initialize() {
   var mapOptions = {
      center: new google.maps.LatLng(40.601203,-8.668173),
      zoom: 2,
      mapTypeId: 'roadmap',
   };

   map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

   // a new Info Window is created
   infoWindow = new google.maps.InfoWindow();

   // Event that closes the Info Window with a click on the map
   google.maps.event.addListener(map, 'click', function() {
      infoWindow.close();
   });

   // Finally displayMarkers() function is called to begin the markers creation
   displayMarkers();
}
google.maps.event.addDomListener(window, 'load', initialize);


// This function will iterate over markersData array
// creating markers with createMarker function
function displayMarkers(){

   // this variable sets the map bounds according to markers position
   var bounds = new google.maps.LatLngBounds();

   // for loop traverses markersData array calling createMarker function for each marker
   for (var i = 0; i < markersData.length; i++){

      var latlng = new google.maps.LatLng(markersData[i].lat, markersData[i].lng);
      var name = markersData[i].domain;

      createMarker(latlng, name);

      // marker position is added to bounds variable
      bounds.extend(latlng);
   }

   // Finally the bounds variable is used to set the map bounds
   // with fitBounds() function
   map.fitBounds(bounds);
}

// This function creates each marker and it sets their Info Window content
function createMarker(latlng, name){
   var marker = new google.maps.Marker({
      map: map,
      position: latlng,
      title: name
   });

   // This event expects a click on a marker
   // When this event is fired the Info Window content is created
   // and the Info Window is opened.
   google.maps.event.addListener(marker, 'click', function() {

      // Creating the content to be inserted in the infowindow
      var iwContent = '<div id="iw_container">' +
            '<div class="iw_title">' + name + '</div>' + '</div>';

      // including content to the Info Window.
      infoWindow.setContent(iwContent);

      // opening the Info Window in the current map and at the current marker location.
      infoWindow.open(map, marker);
   });
}
