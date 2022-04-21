from django.http import HttpResponse
import datetime

def home(request):
    html = '''
    <html>
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
    <center>
    <h1>Treeeeee</h1>
    </center>
    <style type="text/css">
            #mynetwork {
                width: 80%;
                height: 500px;
                border: 1px solid lightgray;
            }
    </style>
    <style>.button {
        border: black;
        color: blueviolet;
        padding: 15px 32px;
        text-align: center;
        display: inline-block;
        font-size: 16px;
        cursor: pointer;
    }
    .button1 {background-color: darksalmon;}
    .button2 {background-color: plum; }
    </style>
    </head>
    <body>
    <div id = "mynetwork"></div>
    <script type="text/javascript">
        // initialize global variables.
        var edges;
        var nodes;
        var network; 
        var container;
        var options, data;
        // This method is responsible for drawing the graph, returns the drawn network
        function drawGraph() {
            var container = document.getElementById('mynetwork');
            // parsing and collecting nodes and edges from the python
            nodes = new vis.DataSet([{"font": {"color": "black"}, "id": 1, "label": "Feliks B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 2, "label": "Franciszek B", "level": 0, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 3, "label": "Bernadyka B", "level": 0, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 4, "label": "Zofia B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 5, "label": "Franciszek B", "level": 1, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 6, "label": "Zenon B", "level": 1, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 7, "label": "Zenon D", "level": 1, "shape": "box", "size": 10}]);
            edges = new vis.DataSet([{"from": 1, "label": 1, "to": 2, "weight": 1}, {"from": 1, "label": 1, "to": 3, "weight": 1}, {"from": 1, "label": 1, "to": 4, "weight": 1}, {"from": 1, "label": 1, "to": 5, "weight": 1}, {"from": 1, "label": 1, "to": 6, "weight": 1}, {"from": 1, "label": 1, "to": 7, "weight": 1}]);
            // adding nodes and edges to the graph
            data = {nodes: nodes, edges: edges};
            var options = {"edges": {"to": {"enabled": true, "type": "arrow"}, "color": {"inherit": true}, "smooth": false}, "layout": {"hierarchical": {"enabled": true, "levelSeparation": 200, "nodeSpacing": 60, "direction": "UD", "sortMethod": "directed"}}, "physics": {"hierarchicalRepulsion": {"centralGravity": 0}, "minVelocity": 0.75, "solver": "hierarchicalRepulsion"}};
            network = new vis.Network(container, data, options);
            return network;
        }
        drawGraph();
    </script>
    <div>
        <button class="button button1">TOUCH ME!</button>
        <button class="button button2">TOUCH ME TOOO!</button>
    </div>
    </body>
    </html>
    '''
    return HttpResponse(html)
