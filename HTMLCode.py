# HTMLCode.py
#
# Justin Norden, Cole Stephan, Sam Keller
#
# This file contains some of the HTML that we use in our index.py file and we didn't want
# that file to look that ugly so here is the ugly html!
#
# A lot of this code is from the Google Developers website and we basically just took it

graphHTML = '''\
<html>
<head>
<!--Load the AJAX API-->
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">

// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

// Create the data table.
var data = new google.visualization.DataTable();
data.addColumn('string', 'Year');
data.addColumn('number', 'GDP');
data.addRows(%s);

// Set chart options
var options = {'title':'GDP Data',
               'width':500,
               'height':300};

// Instantiate and draw our chart, passing in some options.
var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);
}
</script>
</head>

<body>
<!--Div that will hold the pie chart-->
<div id="chart_div"></div>
</body>
</html>'''

tableHeader = '''\
    <html>
    <body>
    
    <table border="1">
      <tr>
        <th>Year</th>
        <th>GDP ($million)</th>
      </tr>
    ''' 

tableHTML = '''\
        <tr>
          <td>%s</td>
          <td>%s</td>
        </tr>
        '''