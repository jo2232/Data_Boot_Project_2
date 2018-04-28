var markers = [];
var coordinates = [];
var zoom = null;
var lat = null;
var lon = null;
var key = null;
var marker = null;
var sum = 0;
var avg = null;
var nat_sum = null;
var nat_avg = null;
var national_sent = [];
var someList = [];
var nameItem = null;
var e = null;
var strCity = null;
var map_coords = [];
var map = null;
let myLayer = null;
let mapboxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
let accessToken = 'pk.eyJ1IjoicmluY2tkIiwiYSI6ImNpamc3ODR1aDAxMmx0c2x0Zm9lc3E1OTAifQ.pIkP7PdJMrR5TBIp93Dlbg';
var dflt = {};
var gg1 = {};


var twitterIcon = L.icon({
    iconUrl: 'https://www.geraldgiles.co.uk/wp-content/uploads/2017/07/twitter-logo-transparent.png',
    // shadowUrl: 'leaf-shadow.png',

    iconSize:     [30,30], // size of the icon
    // shadowSize:   [50, 64], // size of the shadow
    // iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    // shadowAnchor: [4, 62],  // the same for the shadow
    // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

// read in leaflet and start creating map
d3.json("https://gbfs.citibikenyc.com/gbfs/en/station_information.json", createMarkers);


function createMarkers(response) {

    // read in .json
    d3.json("/getLastData", facts)

    //begin parsing through data and separating into dictionaries
    function facts(response) {

        //loop through each city
        for (key in response) {
            tweet_sentiment = []
            // loop through each tweet in each city
            for (var i = 0; i < response[key]['data'].bounding_box.length; i++) {

                // assign lat/lon
                lat = response[key]['data'].bounding_box[i][1];
                lon = response[key]['data'].bounding_box[i][0];

                // create marker
                marker = L.marker([lat, lon], {icon: twitterIcon})
                    .bindPopup("<img src=" + response[key]['data'].profile_image_url[i] + ">" + "<br>"
                    + "<h3>" + response[key]['data'].user[i] + "</h3>"
                    + "<p>" + response[key]['data'].text[i] + "</p>")
                    ;

                // add to list of markers
                markers.push(marker)

                // add tweet sentiment to city list 
                tweet_sentiment.push(response[key]['data'].comp_sent[i])

                // add tweet to national sentiment list
                national_sent.push(response[key]['data'].comp_sent[i])

            }

            // get sentiment average for individual city
            sum = 0;
            for (var i = 0; i < tweet_sentiment.length; i++) {
                sum += parseFloat(tweet_sentiment[i]);
            }


            // assign avg value to variable
            avg = sum / tweet_sentiment.length;

            // loop through cities to make list of name, coordinates, and average sentiment
            if (response.hasOwnProperty(key)) {
                coordinates.push({
                    lon: response[key]['gps'][0],
                    lat: response[key]['gps'][1],
                    city: key,
                    sentiment: avg
                });
            }
        }

        someList = document.getElementById("selDataset");
        length = someList.options.length

        if (length === 0) {
            //manually add default option USA to dropdown list
            someList = document.getElementById("selDataset");
            nameItem = document.createElement("option");
            nameItem.innerHTML = 'USA';
            someList.appendChild(nameItem);

            // populate html dropdown with city names returned from script
            for (var i = 0; i < coordinates.length; i++) {
                var nameItem = document.createElement("option");
                var something = coordinates[i].city;
                nameItem.innerHTML = something;
                someList.appendChild(nameItem);
            };
        }

        // determine map_coords
        e = document.getElementById("selDataset");
        strCity = e.options[e.selectedIndex].text;
        map_coords = [];

        if (strCity === 'USA') {
            map_coords = [39.5, -98.35]
            zoom = 3

            // get sentiment for national average
            nat_sum = 0;
            for (var i = 0; i < national_sent.length; i++) {
                nat_sum += parseFloat(national_sent[i]);
            }
            nat_avg = nat_sum / national_sent.length;
            feels = nat_avg;
        } else {
            for (var i = 0; i < coordinates.length; i++) {
                if (strCity === coordinates[i].city) {
                    map_coords = [coordinates[i].lat, coordinates[i].lon]
                    zoom = 9
                    feels = coordinates[i].sentiment
                }
            }
        }

        // call create map function with marker list
        createMap(L.featureGroup(markers), map_coords, zoom, feels);

    }

}

//create map
function createMap(markers, map_coords, zoom, feels) {
    map = L.map("map-id", {
        center: [map_coords[0], map_coords[1]],
        zoom: zoom,
        layers: [markers]
    });
    myLayer = L.tileLayer(mapboxUrl, { id: 'mapbox.dark', maxZoom: 20, accessToken: accessToken });
    myLayer.addTo(map);
    gauge(feels);
}

//change map coords
function optionChanged(value) {
    if (map) {
        map.remove()
    }
    d3.json("https://gbfs.citibikenyc.com/gbfs/en/station_information.json", createMarkers);
}

function gauge(sent) {
    dflt = {
        min: -1,
        max: 1,
        donut: false,
        gaugeWidthScale: 0.6,
        counter: true,
        hideInnerShadow: true
    }
    if (Object.keys(gg1).length === 0) {
    gg1 = new JustGage({
        title: 'Average Tweet Sentiment',
        id: 'gg1',
        value: sent,
        defaults: dflt,
        decimals: true
    }); 
} else {
    gg1.refresh(sent)
}
}
  







