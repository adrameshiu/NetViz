import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
from pprint import pprint
import math

def parse_nodes_json(nodes_json):
    level = 0
    network_depth = len(nodes_json)
    nodes_heirarchy = []

    for node_catagory_json in nodes_json:
        nodes = []
        node_type = node_catagory_json.get("name")
        nodes_in_catagory = node_catagory_json.get("nodes")
        for node in nodes_in_catagory:
            nodes.append({"label":node, "level":level, "type":node_type})

        nodes_heirarchy.append({level:nodes})
        level = level + 1
    
    return nodes_heirarchy, network_depth

def get_node_positions(nodes_heirarchy, network_depth, height, width):
    origin_level = math.floor(network_depth/2)
    for h in range(0,len(nodes_heirarchy)-1) :
        level = nodes_heirarchy[h][h]
        ypos = (origin_level - h) * height
        mid_level = math.floor(len(level)/2)
        for w in range(0,len(level)-1):
            xpos = math.floor((w - mid_level)/2) + width
            level[w]["pos"] = (xpos,ypos)
    return nodes_heirarchy
def get_weights():
    # Loading the sensory->inter adjacency matrix into a numpy arrays
    sensory2inter_adj_weights = np.loadtxt('datafiles/weights/sensorweights.dat', dtype=float)

    # Loading the interneurons->interneurons adjacency matrix into a numpy array
    inter2inter_adj_weights = np.loadtxt('datafiles/weights/interweights.dat', dtype=float)
    
    # Loading the interneurons->motors adjacency matrix into a numpy array
    inter2motor_adj_weights = np.loadtxt('datafiles/weights/motorweights.dat', dtype=float)
    
    return sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights


def get_node_maps():
    #mapping index(starting from 0) to inter neuron labels

    sensory_neuron_map = {0:{"label":1, "type":"sensory"},
                            1:{"label":2, "type":"sensory"},
                            2:{"label":3, "type":"sensory"},
                            3:{"label":4, "type":"sensory"},
                            4:{"label":5, "type":"sensory"},
                            5:{"label":6, "type":"sensory"},
                            6:{"label":7}, "type":"sensory"}

    inter_neuron_map = {0:{"label":8,"sign":"+","type":"inter", "level":1, "pos":(-40,0)}, 
                            1:{"label":9, "sign":"-", "type":"inter", "level":1, "pos":(-20,0)}, 
                            2:{"label":10,"sign":"+", "type":"inter", "level":1, "pos":(0,0)}, 
                            3:{"label":11,"sign":"+", "type":"inter", "level":1, "pos":(20,0)}, 
                            4:{"label":12,"sign":"+", "type":"inter", "level":1, "pos":(40,0)}}

    motor_neuron_map = {0:{"label":13, "type":"motor", "level":1, "pos":(-20,-20)}, 
                            1:{"label":14, "type":"motor", "level":1, "pos":(20,-20)}}

    return sensory_neuron_map, inter_neuron_map, motor_neuron_map


def get_node_color(node_dict):
    print(node_dict)
    label = node_dict['label'] if 'label' in node_dict else None
    sign = node_dict['sign'] if 'sign' in node_dict else None
    node_type = node_dict['type'] if 'type' in node_dict else None
        
    if ("-" == sign):
        return  0.5714
    elif ("+" == sign):
        return 0.25
    elif (node_type == "motor"):
        return 0.90
    elif (node_type == "sensory"):
        return 1
    else:
        return 0.12


def build_network(nodes_heirarchy, network_depth, sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights):
    nodes_heirarchy = get_node_positions(nodes_heirarchy=nodes_heirarchy,network_depth=network_depth,height=10,width=10)
    sensory_neuron_map, inter_neuron_map, motor_neuron_map = get_node_maps()
    #print(sensory_neuron_map)
    #print(inter_neuron_map)
    #print(motor_neuron_map)
    #sensor_neurons_nodes_list = [v.get('label') for k,v in sensory_neuron_map.items()]
    inter_neurons_nodes_list = [v.get('label') for k,v in inter_neuron_map.items()]
    motor_neurons_nodes_list = [v.get('label') for k,v in motor_neuron_map.items()]

    inter2motor_row_length = inter2motor_adj_weights.shape[0]
    inter2motor_col_length = inter2motor_adj_weights.shape[1]

    G = nx.Graph()
    #pos = nx.random_layout(G)  # positions for all nodes
    

    #networkx nodes
    options = {"node_size": 500, "alpha": 0.8}
    #G.add_nodes_from(G,nodelist=inter_neurons_nodes_list, node_color="r", **options)

    for k, v in inter_neuron_map.items():
        label = v.get('label')
        pos = v.get('pos')
        G.add_node(label, pos=pos)
        
    for k, v in motor_neuron_map.items():
        label = v.get('label')
        pos = v.get('pos')
        G.add_node(label, pos=pos)
        
    #networkx edges
    for motor_index in range(0, inter2motor_col_length):
        for inter_neuron_index in range(0,inter2motor_row_length): 
            inter_neuron = inter_neuron_map[inter_neuron_index].get("label")
            motor_neuron = motor_neuron_map[motor_index].get("label")
            edge_weight = inter2motor_adj_weights[inter_neuron_index][motor_index]
            edge_sign = '+' if edge_weight >=0 else '-'
            edge_color = 'b' if edge_sign == '+' else "g"
            abs_edge_weight = abs(edge_weight)
            print(inter_neuron, motor_neuron, edge_weight, edge_sign, edge_color)
            G.add_edge(inter_neuron,motor_neuron,color=edge_color, weight=abs_edge_weight, alpha=0.5)
        

    values= []
    for node in G.nodes():
        for key, value in inter_neuron_map.items():
            label = value['label'] if 'label' in value else None
            sign = value['sign'] if 'sign' in value else None
            if(node == label):
                values.append(get_node_color(node_dict=value))

        for key, value in motor_neuron_map.items():
            label = value['label'] if 'label' in value else None
            sign = value['sign'] if 'sign' in value else None
            if(node == label):
                values.append(get_node_color(node_dict=value))

    node_colors= nx.get_node_attributes(G,'color').values()
    node_pos= nx.get_node_attributes(G,'pos')
    edge_colors = nx.get_edge_attributes(G,'color').values()
    edge_weights = nx.get_edge_attributes(G,'weight').values()

    nx.draw(G, pos=node_pos, node_color=values,cmap=plt.cm.Reds,edge_color= edge_colors,width= list(edge_weights), with_labels=True)
    plt.show()

# MAIN
def main():
    with open('datafiles/node_def/nodes.json') as json_file:
        node_def = json.load(json_file)

    nodes_heirarchy, network_depth = parse_nodes_json(node_def)
    sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights = get_weights()

    network_inputs = (nodes_heirarchy, network_depth, sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights)
    build_network(*network_inputs)

if __name__ == "__main__":
    main()
