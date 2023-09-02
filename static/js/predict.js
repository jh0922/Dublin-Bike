// handle the prediction data and chart
google.charts.load('current', {'packages':['gauge']});

document.addEventListener('DOMContentLoaded', function() {
document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault(); // prevent the default form submission behavior
    
    document.getElementById("prediction").innerHTML = "Prediction:"
    // get user input value
    var dropdown1 = document.getElementById("selectDropdownPredictStart");
    var selectedStart= dropdown1.options[dropdown1.selectedIndex].value;
    
    var dropdown2 = document.getElementById("selectDropdownPredictDest");
    var selectedDest= dropdown2.options[dropdown2.selectedIndex].value;


    var dateString = document.getElementById('datetime').value;
    var datetime = new Date(dateString);
    var hour = datetime.getHours(); // get the hour (0-23)
    let day = datetime.getDate(); // get the day of the month (1-31)
    var month = datetime.getMonth() + 1; // get the month (0-11), and add 1 to convert to 1-12
    var realdate;

    // return user input value to Flask
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'hour=' + encodeURIComponent(hour) + '&day=' + encodeURIComponent(day) + '&month=' + encodeURIComponent(month) + '&selectedStart=' + encodeURIComponent(selectedStart) + '&selectedDest=' + encodeURIComponent(selectedDest) 
    })
    .then(response => {
      if (response.status === 200) {
        return response.text()
      } else {
        throw new Error();
      }
    })
    // fetch Flask response data to handle prediction
    .then(data =>{
      data = JSON.parse(data);
      realdate=(data[2]);


      // starting station available bikes prediction chart
      var chart_data = new google.visualization.DataTable();
      chart_data.addColumn('number', 'Time of Day');
      chart_data.addColumn('number', 'available_bikes');
      chart_data.addRow([1, parseInt(JSON.parse(data[0]))]);
      var options = {
          title: 'Available Bikes at Starting Point',
          legend:"none",
          colors: ['#68DE9B'],
          animation:{
              duration:1000,
              easing: 'out',
              startup:true
          },                  
          hAxis: {
          // title: 'Time of Day(24hrs)',
          baselineColor:"transparent"
          },
          vAxis: {
          title: 'Number of Bikes',
          }
          };

      var chart = new google.visualization.ColumnChart(
          document.getElementById('predict_1'));

      chart.draw(chart_data, options);


      // destination available bikes stands prediction chart
      var chart_data = new google.visualization.DataTable();
      chart_data.addColumn('number', 'Time of Day');
      chart_data.addColumn('number', 'available_bikes_stand');
      chart_data.addRow([1, parseInt(JSON.parse(data[1]))]);
      var options = {
          title: 'Available Bikes Stands at Destination',
          legend:"none",
          colors: ['#68DE9B'],
          animation:{
              duration:1000,
              easing: 'out',
              startup:true
          },                  
          hAxis: {
          baselineColor:"transparent"
          },
          vAxis: {
          title: 'Number of Bikes Stands',
          }
          };

      var chart = new google.visualization.ColumnChart(
          document.getElementById('predict_2'));

      chart.draw(chart_data, options);

  


  // fetch weather forecast data and choose the data that matched the user input day
  fetch("/weatherforecast")
  .then((response) => response.json())
  .then(data => { 
    var temp;
    var realfeel;
    var speed;
    var humidity;
    var description;
    var icon;


    data.list.forEach((day)=>{
      const date = new Date(day.dt * 1000);
      if (date.getDate() == realdate){
      temp = (day.temp.day-273.15).toFixed(1)
      realfeel = (day.feels_like.day-273.15).toFixed(1)
      speed = day.speed
      humidity = day.humidity
      description = day.weather[0].description
      icon = day.weather[0].icon
    
      document.getElementById("description").innerHTML = description;
    }  
  })

    // draw the weather forecast into chart
    // intital values of 0 to mimic the startup animation
    var data = google.visualization.arrayToDataTable([
      ['Label', 'Value'],
      ['temp(℃)', 0],
      ['real feel(℃)', 0],
      ['speed(m/s)', 0],
      ['humidity(%)', 0]
    ]);

    var options = {
      width: 400, height: 120,
      minorTicks: 5
    };

    var chart = new google.visualization.Gauge(document.getElementById('meter'));
    //console.log(chart);
    chart.draw(data, options);

    data.setValue(0,1,parseFloat(temp));
    data.setValue(1,1,parseFloat(realfeel));
    data.setValue(2,1,speed);
    data.setValue(3,1,humidity);
  
    setTimeout(function() {
      chart.draw(data, options);
    }, 500);

    // weather icon;
    var iconUrl = `http://openweathermap.org/img/wn/${icon}.png`;
    document.getElementById("icon").src = iconUrl;
    document.getElementById("icon").height = 75;
    document.getElementById("icon").width = 100;
  })
  .catch(error => {
  console.log(error);
  });
});
  })
})  