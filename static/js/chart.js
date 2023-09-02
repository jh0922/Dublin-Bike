// file create the history chart for stations
google.charts.load('current', {packages: ['corechart', 'bar']});
window.onload = google.charts.setOnLoadCallback(draw);


function draw() {
    // get user input stations
  selectDropdown = document.getElementById("dropdownHistory").getElementsByTagName("select");
  for (let i = 0; i < selectDropdown.length; i++) {
      selectDropdown[i].addEventListener("change", function() {
      const url_7 = `/history7/${selectDropdown[i].value}`;
      const url_24 = `/history24/${selectDropdown[i].value}`;

      // draw chart for 7 days

      fetch(url_7)
        .then((response) =>  response.json())
        .then(data => { 
        data = JSON.parse(data.data_24);

    //   create datatable and insert the value for charts
      var chart_data = new google.visualization.DataTable();
      var hAxisLabels = ["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"];
      chart_data.addColumn('string', 'Day');
      chart_data.addColumn('number', 'available_bikes');
      for (const row of data){
      chart_data.addRow([hAxisLabels[data.indexOf(row)], row[1]]);
      }

    //   set the chart options
      var options = {
          title: 'Average bikes available per day',
          legend:"none",
          colors: ['#BEDE68'],
          animation:{
              duration:1000,
              easing: 'out',
              startup:true
          },          
          hAxis: {
              title: 'Day',
              baselineColor:"transparent"
          },
          vAxis: {
              title: 'Number of Bikes',
              viewwindow:{
                  min:10
              }
          }
          };
  
          var chart = new google.visualization.ColumnChart(
          document.getElementById('myChart_7'));
  
          chart.draw(chart_data, options);
      }) 
      
    // draw chart for 24 hours
      fetch(url_24)
      .then((response) =>  response.json())
      .then(data => { 
         
          data = JSON.parse(data.data_24);

    //   create datatable and insert the value for charts
      var chart_data = new google.visualization.DataTable();
      chart_data.addColumn('number', 'Time of Day');
      chart_data.addColumn('number', 'available_bikes');
      for (const row of data){
      chart_data.addRow([data.indexOf(row), row[1]]);
          }

    //   set the chart options
      var options = {
          title: 'Average bikes available per hour',
          legend:"none",
          colors: ['#68DE9B'],
          animation:{
              duration:1000,
              easing: 'out',
              startup:true
          },                  
          hAxis: {
          title: 'Time of Day(24hrs)',
          baselineColor:"transparent"
          },
          vAxis: {
          title: 'Number of Bikes',
          }
          };

      var chart = new google.visualization.ColumnChart(
          document.getElementById('myChart_24'));

      chart.draw(chart_data, options);
  })
 })}}