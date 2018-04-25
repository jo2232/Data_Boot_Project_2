d3.json("https://gbfs.citibikenyc.com/gbfs/en/station_information.json", createMarkers);


function createMarkers(response) {
    let demographics = response
    var markers = [];
    var sentiments = [];
    d3.json("/twitterize", facts)
    function facts(response) {
      console.log(response)
        for (var i = 0; i < response.bounding_box.length; i++) {
            var lat = response.bounding_box[i][1];
            var lon = response.bounding_box[i][0];
            var sent = response.comp_sent[i]
            sentiments.push(sent)
            let marker = L.marker([lat, lon]).on("click", gauge())
                .bindPopup("<img src=" + response.profile_image_url[i] + ">" + "<br>"
                          +  "<h3>" + response.user[i] + "</h3>" 
                          +  "<p>" + response.text[i] + "</p>")
                          ;
            markers.push(marker)      
    }
    // console.log(markers)
    createMap(L.featureGroup(markers));
}
}


function createMap(markers) {
    var map = L.map("map-id", {
        center: [32.776664, -96.796988],
        zoom: 9,
        layers: [markers]
    });
    let mapboxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
    let accessToken = 'pk.eyJ1IjoicmluY2tkIiwiYSI6ImNpamc3ODR1aDAxMmx0c2x0Zm9lc3E1OTAifQ.pIkP7PdJMrR5TBIp93Dlbg';
    let myLayer = L.tileLayer(mapboxUrl, { id: 'mapbox.dark', maxZoom: 20, accessToken: accessToken });
    myLayer.addTo(map);
}


function gauge(sent) {
    
        var dflt = {
          min: 0,
          max: 1,
          donut: false,
          gaugeWidthScale: 0.6,
          counter: true,
          hideInnerShadow: true
        }
    
        var gg1 = new JustGage({
          id: 'gg1',
          value: sent,
          title: 'Tweet Happiness',
          defaults: dflt
        });
      }
    

    
 