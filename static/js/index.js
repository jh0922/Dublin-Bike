// function to initiate google map and create interactivity between maps and dropdown menu
function initAutocomplete() {
    fetch("/stations")
        .then((response) => response.json())
        .then(data => {
            // create map
            const dublin = {lat: 53.350140, lng: -6.266155};
            var map = new google.maps.Map(document.getElementById('map'), {center: dublin, zoom: 13});

            // set a bicyclinglayer to the map
            const bikeLayer = new google.maps.BicyclingLayer();
            bikeLayer.setMap(map);

            const directionsService = new google.maps.DirectionsService();
            const directionsRenderer = new google.maps.DirectionsRenderer();
            directionsRenderer.setMap(map);
            const onChangeHandler = function () {
                const travelMode = document.getElementById("travelMode").value;
              calculateAndDisplayRoute(directionsService, directionsRenderer, travelMode);
            };
          
            document.getElementById("selectDropdownPredictStart").addEventListener("change", onChangeHandler);
            document.getElementById("selectDropdownPredictDest").addEventListener("change", onChangeHandler);
            document.getElementById("travelMode").addEventListener("change", onChangeHandler);

          
            const greenIcon = {
                url: '../static/images/green.jpg',
                scaledSize: new google.maps.Size(25, 35), // set the size of the icon
              };

            const redIcon = {
            url: '../static/images/red.jpg',
            scaledSize: new google.maps.Size(25, 35), // set the size of the icon
            };
            
            const orangeIcon = {
                url: '../static/images/orange.jpg',
                scaledSize: new google.maps.Size(25, 35), // set the size of the icon
                };

            // create marker and infowindow for each station
            for (const station of data.stations) {
                window.setTimeout(() => {
                    var icon;
                        if(station.available_bikes>=14){
                            icon = greenIcon;
                        }
                        else if(station.available_bikes>7 && station.available_bikes<14){
                            icon = orangeIcon;
                        }
                        else {
                            icon = redIcon;
                        };


                    marker = new google.maps.Marker({
                        position: {lat:station.position_lat, lng: station.position_lng},
                        map: map,
                        icon: icon,
                        animation: google.maps.Animation.DROP,
                        title: station.number.toString()
                    });

                    var infowindow = new google.maps.InfoWindow({
                        content:("<h2>" + station.name + "</h2>"
                        + "<p><b>Status: </b>" + station.status + "</p>"
                        + "<p><b>Total Bikes Stands: </b>" + station.bike_stands + "</p>"
                        + "<p><b>Available Stands: </b>" + station.available_bikes_stands + "</p>"
                        + "<p><b>Available Bikes: </b>" + station.available_bikes + "</p>"
                        + "<p><b>Last Update: </b>" + station.last_update + "</p>")
                    })


                    // set the click function on the marker
                    marker.addListener("click", () => {
                    infowindow.open(map,marker);
                    infowindow.setPosition({lat: station.position_lat, lng: station.position_lng});
                })
            }, data.stations.indexOf(station) * 10)
            
            }
            

            // when user select the starting station, the station details associated with it will show on the map
            var dropdown = document.getElementById("selectDropdownPredictStart");
            // For the selectDropdownPredictStart dropdown
            dropdown.addEventListener("change", function () {
            var selectedValue = this.value;
        
            const rightstation = data.stations.find((data) => parseInt(data.number) == selectedValue);
            var infowindow = new google.maps.InfoWindow({
                content:("<h2>" + rightstation.name + "</h2>"
                + "<p><b>Status: </b>" + rightstation.status + "</p>"
                + "<p><b>Total Bikes Stands: </b>" + rightstation.bike_stands + "</p>"
                + "<p><b>Available Stands: </b>" + rightstation.available_bikes_stands + "</p>"
                + "<p><b>Available Bikes: </b>" + rightstation.available_bikes + "</p>"
                + "<p><b>Last Update: </b>" + rightstation.last_update + "</p>")
            })
            infowindow.setPosition({lat: rightstation.position_lat, lng: rightstation.position_lng});
            map.setCenter({lat: rightstation.position_lat, lng: rightstation.position_lng})
            map.setZoom(16);
            infowindow.open(map);
            })

            // when user select the destination station, the station details associated with it will show on the map
            var dropdown = document.getElementById("selectDropdownPredictDest");
            // For the selectDropdownPredictDest dropdown
            dropdown.addEventListener("change", function () {
            var selectedValue = this.value;

            const rightstation = data.stations.find((data) => parseInt(data.number) == selectedValue);
            var infowindow = new google.maps.InfoWindow({
                content:("<h2>" + rightstation.name + "</h2>"
                + "<p><b>Status: </b>" + rightstation.status + "</p>"
                + "<p><b>Total Bikes Stands: </b>" + rightstation.bike_stands + "</p>"
                + "<p><b>Available Stands: </b>" + rightstation.available_bikes_stands + "</p>"
                + "<p><b>Available Bikes: </b>" + rightstation.available_bikes + "</p>"
                + "<p><b>Last Update: </b>" + rightstation.last_update + "</p>")
            })
            infowindow.setPosition({lat: rightstation.position_lat, lng: rightstation.position_lng});
            map.setCenter({lat: rightstation.position_lat, lng: rightstation.position_lng})
            map.setZoom(14);
            infowindow.open(map);



             // when user select the destination station, the station details associated with it will show on the map
             var dropdown = document.getElementById("selectDropdownHistory");
             dropdown.addEventListener("change", function () {
             var selectedValue = this.value;
 
             const rightstation = data.stations.find((data) => parseInt(data.number) == selectedValue);
             var infowindow = new google.maps.InfoWindow({
                 content:("<h2>" + rightstation.name + "</h2>"
                 + "<p><b>Status: </b>" + rightstation.status + "</p>"
                 + "<p><b>Total Bikes Stands: </b>" + rightstation.bike_stands + "</p>"
                 + "<p><b>Available Stands: </b>" + rightstation.available_bikes_stands + "</p>"
                 + "<p><b>Available Bikes: </b>" + rightstation.available_bikes + "</p>"
                 + "<p><b>Last Update: </b>" + rightstation.last_update + "</p>")
             })
             infowindow.setPosition({lat: rightstation.position_lat, lng: rightstation.position_lng});
             map.setCenter({lat: rightstation.position_lat, lng: rightstation.position_lng})
             map.setZoom(17);
             infowindow.open(map);       
             })




            // Add the search box
            const searchBox = new google.maps.places.SearchBox(document.getElementById("search-box"));

            // Add the 'places_changed' event listener to the search box
            searchBox.addListener('places_changed', () => {
                const places = searchBox.getPlaces();

                if (places.length === 0) {
                    return;
                }

                const bounds = new google.maps.LatLngBounds();
                places.forEach((place) => {
                    if (place.geometry.viewport) {
                        bounds.union(place.geometry.viewport);
                    } else {
                        bounds.extend(place.geometry.location);
                    }
                });
                map.fitBounds(bounds);
            });
        
    })}
        )}

    function calculateAndDisplayRoute(directionsService, directionsRenderer, travelMode) {
      directionsService
        .route({
          origin: {
            query: (document.getElementById("selectDropdownPredictStart").options[document.getElementById("selectDropdownPredictStart").selectedIndex].getAttribute('data-value2'))+","+(document.getElementById("selectDropdownPredictStart").options[document.getElementById("selectDropdownPredictStart").selectedIndex].getAttribute('data-value3'))
          },
          destination: {
            query: (document.getElementById("selectDropdownPredictDest").options[document.getElementById("selectDropdownPredictDest").selectedIndex].getAttribute('data-value2'))+","+(document.getElementById("selectDropdownPredictDest").options[document.getElementById("selectDropdownPredictDest").selectedIndex].getAttribute('data-value3'))
          },
          travelMode: google.maps.TravelMode[travelMode],
        })
        .then((response) => {
          directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + e));
    }



let map;
window.initAutocomplete = initAutocomplete;

