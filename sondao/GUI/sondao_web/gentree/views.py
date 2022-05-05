from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import PersonForm
from .models import Person


def person_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PersonForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.surname = form.cleaned_data['surname']
            post.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PersonForm()

    return render(request, 'form.html', {'form': form})


def home(request):
    html = '''
    <html>
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
    <center>
    <h1>Treeeeee</h1>
    </center>
    <!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
    <script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
    <style type="text/css">
    
            #mynetwork {
                width: 100%;
                height: 600px;
                background-color: white;
                border: 1px solid lightgray;
                position: relative;
                float: left;
            }
    
            .button {
                  border: none;
                  color: white;
                  padding: 15px 32px;
                  text-align: center;
                  text-decoration: none;
                  display: inline-block;
                  font-size: 16px;
                  margin: 4px 2px;
                  cursor: pointer;
                }
    
            .button1 {background-color: #4CAF50;} /* Green */
            .button2 {background-color: #008CBA;} /* Blue */
            .button1 {
                  background-color: white;
                  color: black;
                  border: 2px solid #4CAF50;
            }
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
            nodes = new vis.DataSet([{"font": {"color": "black"}, "id": 1, "label": "Feliks B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 2, "label": "Franciszek B", "level": 0, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 3, "label": "Bernadyka B", "level": 0, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 4, "label": "Zofia B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 5, "label": "Franciszek B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 6, "label": "Zenon B", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 7, "label": "Zenon D", "level": 1, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 8, "label": "Agnieszka B", "level": 2, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 9, "label": "Krystyna J", "level": 2, "physics": false, "shape": "box", "size": 10}, {"font": {"color": "black"}, "id": 10, "label": "Gra\u017cyna (Grace) G", "level": 2, "physics": false, "shape": "box", "size": 10}]);
            edges = new vis.DataSet([{"from": 1, "label": 1, "to": 2, "weight": 1}, {"from": 1, "label": 1, "to": 3, "weight": 1}, {"from": 1, "label": 1, "to": 4, "weight": 1}, {"from": 1, "label": 1, "to": 5, "weight": 1}, {"from": 1, "label": 1, "to": 6, "weight": 1}, {"from": 1, "label": 1, "to": 7, "weight": 1}, {"from": 5, "label": 1, "to": 8, "weight": 1}, {"from": 5, "label": 1, "to": 9, "weight": 1}, {"from": 5, "label": 1, "to": 10, "weight": 1}]);
            // adding nodes and edges to the graph
            data = {nodes: nodes, edges: edges};
            var options = {"edges": {"to": {"enabled": true, "type": "arrow"}, "color": {"inherit": true}, "smooth": false}, "layout": {"hierarchical": {"enabled": true, "levelSeparation": 200, "nodeSpacing": 100, "direction": "UD", "sortMethod": "directed"}}, "physics": {"hierarchicalRepulsion": {"centralGravity": 0}, "minVelocity": 0.75, "solver": "hierarchicalRepulsion"}};
            network = new vis.Network(container, data, options);
            return network;
        }
        drawGraph();
    </script>
    <button class="button button2">CLICK ME!</button>
    <button class="button button2">NO! CKLICK ME!</button>
    </body>
    </html>
    '''
    return HttpResponse(html)
