# NetViz
## Purpose

Visualize neural networks into a hierarchical graph using NetworkX. 

Weights and signs will be respected.



## Motivation

While analyzing a neuron network layout, to fully comprehend the network, it is important to segregate the source, interneurons and target neurons. Another thing of importance is the direction and sign of the weights of the synapses. 

Additionally, we might have connections within the interneurons themselves.

This is just a small tool to read a set of neurons, respect the neuron and synapse definitions and show them on a network whose edges are proportional to the weights and are colored based on the signs of the weights.



## Screenshots

![Network Hierarchy](/screenshots/network.JPG)

![Inter Neurons](/screenshots/inter_neuron.JPG)

## Usage

## Activate Virtual Environment
- A virtual environment `netviz-venv` has been created to overcome any dependency issues.
- To activate this virtual environment, use the command 

```
netviz-venv\Scripts\activate.bat
```

> Was created with the command  `python -m venv netviz-venv` 

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

The layouts can also be organized by using the multi-patriate layouts in networkx.

## Credits

The entire project was done under the guidance of Professor Eduardo J Izquierdo at Indiana University Bloomington. I hope that I could be as lively, enthusiastic, and energetic as him in the projects I get to work on. None of this would have been possible if not for his support, ideas, patience and freedom given. Thank You!