// create all the dropdowns in the page
fetch("/stations")
    .then((response) =>  response.json())
    .then(data => { 
        // Create a station dropdown to show history value
        selectDropdownHistory = document.getElementById("selectDropdownHistory")

        // Create station dropdowns to show predicted value
        selectDropdownPredictStart = document.getElementById("selectDropdownPredictStart")
        selectDropdownPredictDest = document.getElementById("selectDropdownPredictDest")


        // Loop through the data and create an option element for each item
        data.stations.forEach((item) => {

            // dropdown for history data of stations
            const optionHistory = document.createElement('option');
            optionHistory.text = item.name;
            optionHistory.value = item.number;
            selectDropdownHistory.appendChild(optionHistory);
            document.getElementById("dropdownHistory").appendChild(selectDropdownHistory);
            

            // dropdown for prediction starting stations
            const optionPredictStart = document.createElement('option');
            optionPredictStart.text = item.name;
            optionPredictStart.value = item.number;
            optionPredictStart.setAttribute('data-value2', item.position_lat);
            optionPredictStart.setAttribute('data-value3', item.position_lng);
            selectDropdownPredictStart.appendChild(optionPredictStart);
            document.getElementById("dropdownPredict").appendChild(selectDropdownPredictStart);
            

            // dropdown for prediction destination stations
            const optionPredictDest = document.createElement('option');
            optionPredictDest.text = item.name;
            optionPredictDest.value = item.number;
            optionPredictDest.setAttribute('data-value2', item.position_lat);
            optionPredictDest.setAttribute('data-value3', item.position_lng);
            selectDropdownPredictDest.appendChild(optionPredictDest);
            document.getElementById("dropdownPredict").appendChild(selectDropdownPredictDest);
             }
        )});



                
            
            


            
