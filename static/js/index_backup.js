function initMap() {
    fetch("/stations")
        .then((response) =>  response.json())
        .then(data => {

            const dublin = {lat: 53.350140, lng: -6.266155 };
            map = new google.maps.Map(document.getElementById('map'), {center:dublin,zoom:13});

            const bikeLayer = new google.maps.BicyclingLayer();
            bikeLayer.setMap(map);
            
            const infowindow = new google.maps.InfoWindow();

            for (const station of data.stations){
                    window.setTimeout(()=>{
                    marker = new google.maps.Marker({
                    position: {lat: station.position_lat, lng: station.position_lng},
                    map: map,
                    animation: google.maps.Animation.DROP,
                    title: station.name
                    });



                marker.addListener("click", () => {

                    infowindow.setContent ("<h2>" + station.name + "</h2>"
                    + "<p><b>Status: </b>" + station.status + "</p>"
                    + "<p><b>Total Bikes Stands: </b>" + station.bike_stands + "</p>"
                    // + "<p><b>position: </b>" + station.position_lat + ", " + station.position_lng + "</p>"
                    + "<p><b>Available Stands: </b>" + station.available_bikes_stands + "</p>"
                    + "<p><b>Available Bikes: </b>" + station.available_bikes + "</p>"
                    + "<p><b>Last Update: </b>" + station.last_update + "</p>")

                    infowindow.open(map);
                    infowindow.setPosition({lat: station.position_lat, lng: station.position_lng});
                })
            },data.stations.indexOf(station)*10)
            }
        }
    )







}



let map;
window.initMap =initMap;


