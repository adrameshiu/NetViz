# NetViz
## Purpose

Visualize neural networks into a hierarchical graph using NetworkX. 

Weights and signs will be respected.

## Usage

### Node Definition 

- Define the nodes that are required in the graph(along with the type/level of node) in a JSON file under the path `datafiles/nodes.json`

- The nodes will be listed as a dictionary with a key that specifies the `type` and a `nodes` key that contain the list of nodes

  ```json
  [
  {"nodes":[1,2,3,4,5,6,7], "name":"sensory"},
  {"nodes":[8,9,10,11,12], "name":"inter"},
  {"nodes":[13,14], "name":"motor"}
  ]
  ```

### Edges Definition

- Define the edges by using adjacency matrixes to represent the edges between nodes of sections
- Define the `datafiles/edge_files.json` as a list of dictionaries containing the `from` and `to` section and the `path` defined as the path to the data file containing their corresponding adjacency matrices

```json
[
{"path":"datafiles/weights/sensorweights.dat", "columns_section":"inter","rows_section":"sensory"},
{"path":"datafiles/weights/interweights.dat", "columns_section":"inter","rows_section":"inter"},
{"path":"datafiles/weights/motorweights.dat", "columns_section":"motor","rows_section":"inter"}
]
```



## Scope

There are still complications where the edges between nodes of the same section are just shown as linear lines along the X axis which are pointless.

This can be overcome by using arc's and representing the networkx graph(exported to a json file) on a D3.js graph. 

## Useful Links

https://www.d3-graph-gallery.com/graph/arc_template.html

https://andrewmellor.co.uk/blog/articles/2014/12/14/d3-networks/