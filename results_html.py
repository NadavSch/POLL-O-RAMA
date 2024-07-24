results_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Survey Results</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawCharts);

      function drawCharts() {
        var aggregatedData = JSON.parse('{{ aggregated_data | safe }}');

        for (let [ageGroup, data] of Object.entries(aggregatedData)) {
          // Data for the exercise pie chart
          var dataQ2 = new google.visualization.DataTable();
          dataQ2.addColumn('string', 'Exercise Frequency');
          dataQ2.addColumn('number', 'Count');
          for (let [exercise, count] of Object.entries(data.exercise)) {
            dataQ2.addRow([exercise, count]);
          }
          var optionsQ2 = {
            title: 'Exercise Frequency - Age Group ' + ageGroup,
            is3D: true,
          };
          var chartQ2 = new google.visualization.PieChart(document.getElementById('piechart_q2_' + ageGroup.replace(/\+/g, 'plus').replace(/\-/g, '_')));
          chartQ2.draw(dataQ2, optionsQ2);

          // Data for the health pie chart
          var dataQ3 = new google.visualization.DataTable();
          dataQ3.addColumn('string', 'Health Rating');
          dataQ3.addColumn('number', 'Count');
          for (let [health, count] of Object.entries(data.health)) {
            dataQ3.addRow([health, count]);
          }
          var optionsQ3 = {
            title: 'Health Rating - Age Group ' + ageGroup,
            is3D: true,
          };
          var chartQ3 = new google.visualization.PieChart(document.getElementById('piechart_q3_' + ageGroup.replace(/\+/g, 'plus').replace(/\-/g, '_')));
          chartQ3.draw(dataQ3, optionsQ3);
        }
      }
    </script>
    <style>
      .chart-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        margin-bottom: 40px;
      }
      .chart {
        width: 45%;
        height: 300px;
        margin-bottom: 20px;
      }
    </style>
</head>
<body>
    <h1>Survey Results</h1>

    <h2>Exercise Frequency</h2>
    <div class="chart-container">
        <div id="piechart_q2_18_25" class="chart"></div>
        <div id="piechart_q2_26_35" class="chart"></div>
        <div id="piechart_q2_36_45" class="chart"></div>
        <div id="piechart_q2_46plus" class="chart"></div>
    </div>

    <h2>Health Rating</h2>
    <div class="chart-container">
        <div id="piechart_q3_18_25" class="chart"></div>
        <div id="piechart_q3_26_35" class="chart"></div>
        <div id="piechart_q3_36_45" class="chart"></div>
        <div id="piechart_q3_46plus" class="chart"></div>
    </div>
</body>
</html>
'''