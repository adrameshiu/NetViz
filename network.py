import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
from pprint import pprint
import math
import pandas as pd
from networkx.readwrite import json_graph

###
#Parse the nodes json under 'datafiles/nodes.json' that contains infromation of the level name and nodes in each level
###
def parse_nodes_json(nodes_json):
    level = 0
    network_depth = len(nodes_json)
    nodes_heirarchy = []
    all_nodes = []

    for node_catagory_json in nodes_json:
        nodes = []
        node_type = node_catagory_json.get("name")
        nodes_in_catagory = node_catagory_json.get("nodes")
        for node in nodes_in_catagory:
            node_dict = {"label":node, "level":level, "type":node_type, "node_index":(len(all_nodes)+1)}
            nodes.append(node_dict)
            all_nodes.append(node_dict)

        nodes_heirarchy.append({level:nodes})
        level = level + 1
    return nodes_heirarchy, all_nodes, network_depth

###
# Parse the options json under 'settings/options.json' that contains infromation about the different setting options like height and width between 
# two nodes
###
def parse_options_json(options_json):
    node_cmap = options_json["node_cmap"] if "node_cmap" in options_json else plt.cm.Greens #setting default value
    edge_cmap = options_json["edge_cmap"] if "edge_cmap" in options_json else plt.cm.Set2
    height = options_json["height"] if "height" in options_json else None
    width = options_json["width"] if "width" in options_json else None

    return node_cmap, edge_cmap, height, width

###
# Using the levels of each section of nodes, and the height and width from settings, 
# find the position of each node in terms of x and y co ordinates and add them to the 'pos' key of each node
# The middle section will be centered at y=0 and the layers above and below will be incremented by the height paramter
# The middle node of each section will be centered at x=0 and the nodes to the left and right will be incremented by the width paramter
###
def get_node_positions(nodes_heirarchy, network_depth, height=10, width=10):
    print(height, width)
    origin_level = math.floor(network_depth/2)
    for h in range(0,len(nodes_heirarchy)) :
        level = nodes_heirarchy[h][h]
        ypos = (origin_level - h) * height
        mid_level = math.floor(len(level)/2)
        for w in range(0,len(level)):
            xpos = math.floor((w - mid_level)) + width
            level[w]["pos"] = (xpos,ypos)
    return nodes_heirarchy


###
# Use the 'datafiles/edge_files.json' to find the path to the *.dat files 
# that contain the path to the edges defined along with their from and to sections they connect. 
###
def get_weights_from_file(edge_files_list, all_nodes):
    all_labels = [node['label'] for node in all_nodes]
    complete_adjacency_matrix =  pd.DataFrame(columns=all_labels, index=all_labels)
    
    for edge_section in edge_files_list:
        file_path = edge_section['path'] 
        from_section_label = edge_section['columns_section']
        to_section_label = edge_section['rows_section']
        
        from_nodes_labels = [node['label'] for node in all_nodes if node['type']==from_section_label]
        to_nodes_labels = [node['label'] for node in all_nodes if node['type']==to_section_label]
  
        file_adj_weights = np.loadtxt(file_path,dtype=float)
        print(from_nodes_labels)
        print(to_nodes_labels)
        pprint(file_adj_weights)
        file_df = pd.DataFrame(file_adj_weights, columns=from_nodes_labels, index=to_nodes_labels)

        for from_node in from_nodes_labels:
            for to_node in to_nodes_labels:
                complete_adjacency_matrix.loc[to_node,from_node] = file_df.loc[to_node,from_node]

    return complete_adjacency_matrix

###
# Build and visualize the network based on the nodes and edges
###
def build_network(nodes_heirarchy, all_nodes, network_depth, complete_adjacency_matrix, height, width, node_cmap, edge_cmap):

    nodes_heirarchy = get_node_positions(nodes_heirarchy=nodes_heirarchy,network_depth=network_depth, height=height, width=width)
    
    pprint(all_nodes)
    #instantiate networkx graph
    G = nx.Graph()

    #networkx nodes
    options = {"node_size": 500, "alpha": 0.8}
    for node in all_nodes:
        label =node.get('label')
        pos = node.get('pos')
        G.add_node(label, pos=pos)
    
    node_color_values= []
    for node in G.nodes():
        node_color_values.append(1) #color scale value for nodes set to max

    node_colors= nx.get_node_attributes(G,'color').values()
    node_pos= nx.get_node_attributes(G,'pos')

    # #networkx edges
    for node1 in all_nodes:
        for node2 in all_nodes: 
            node1_label = node1.get("label")
            node2_label = node2.get("label")
            edge_weight = complete_adjacency_matrix.loc[node1_label,node2_label]
            if not math.isnan(edge_weight): #if there is a value in the complete adj matrix for the edge
                edge_sign = '+' if edge_weight >=0 else '-'
                #edge_color = 'b' if edge_sign == '+' else "g"
                edge_color = 1 if edge_sign == '+' else 0.8
                abs_edge_weight = abs(edge_weight)
                G.add_edge(node1_label,node2_label,color=edge_color, weight=abs_edge_weight, alpha=0.5)
            
    edge_colors = nx.get_edge_attributes(G,'color').values()
    edge_weights = nx.get_edge_attributes(G,'weight').values()

    #draw networkx map
    nx.draw(G, pos=node_pos, node_color=node_color_values, cmap=node_cmap, edge_cmap=edge_cmap, edge_color= edge_colors,width= list(edge_weights), with_labels=True)
    # nx.draw_networkx_edges(
    #     G, node_pos,
    #     connectionstyle="'arc3, rad = 840"  # <-- THIS IS IT
    # )

    #storing data in a json for d3
    data = json_graph.node_link_data(G)
    with open('graph_out.json', 'w') as f:
        json.dump(data, f, indent=4)

#     open window to show plot
    plt.show()


###
# MAIN FUNCTION
##
def main():
    with open('datafiles/nodes.json') as json_file:
        node_def = json.load(json_file)

    with open('datafiles/edge_files.json') as json_file:
        edge_files_list = json.load(json_file)
    
    with open('settings/options.json') as json_file:
        options_json = json.load(json_file)

    nodes_heirarchy, all_nodes, network_depth = parse_nodes_json(node_def)
    node_cmap, edge_cmap, height, width = parse_options_json(options_json)

    complete_adjacency_matrix = get_weights_from_file(edge_files_list, all_nodes)
    network_inputs = (nodes_heirarchy, all_nodes, network_depth, complete_adjacency_matrix, height, width, node_cmap, edge_cmap)
    build_network(*network_inputs)

if __name__ == "__main__":
    main()

##########################################################################################################################################
#UNUSED
#
# def get_node_color(node_dict):
#     print(node_dict)
#     label = node_dict['label'] if 'label' in node_dict else None
#     sign = node_dict['sign'] if 'sign' in node_dict else None
#     node_type = node_dict['type'] if 'type' in node_dict else None
        
#     if ("-" == sign):
#         return  0.5714
#     elif ("+" == sign):
#         return 0.25
#     elif (node_type == "motor"):
#         return 0.90
#     elif (node_type == "sensory"):
#         return 1
#     else:
#         return 0.12
#
# def get_weights():
#     # Loading the sensory->inter adjacency matrix into a numpy arrays
#     sensory2inter_adj_weights = np.loadtxt('datafiles/weights/sensorweights.dat', dtype=float)
#     # Loading the interneurons->interneurons adjacency matrix into a numpy array
#     inter2inter_adj_weights = np.loadtxt('datafiles/weights/interweights.dat', dtype=float)
#     # Loading the interneurons->motors adjacency matrix into a numpy array
#     inter2motor_adj_weights = np.loadtxt('datafiles/weights/motorweights.dat', dtype=float)
#     return sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights
#
# def build_network2(nodes_heirarchy, network_depth, sensory2inter_adj_weights, inter2inter_adj_weights, inter2motor_adj_weights):
#     nodes_heirarchy = get_node_positions(nodes_heirarchy=nodes_heirarchy,network_depth=network_depth,height=10,width=10)
#     sensory_neuron_map, inter_neuron_map, motor_neuron_map = get_node_maps()
#     #print(sensory_neuron_map)
#     #print(inter_neuron_map)
#     #print(motor_neuron_map)
#     #sensor_neurons_nodes_list = [v.get('label') for k,v in sensory_neuron_map.items()]
#     inter_neurons_nodes_list = [v.get('label') for k,v in inter_neuron_map.items()]
#     motor_neurons_nodes_list = [v.get('label') for k,v in motor_neuron_map.items()]

#     inter2motor_row_length = inter2motor_adj_weights.shape[0]
#     inter2motor_col_length = inter2motor_adj_weights.shape[1]

#     G = nx.Graph()
#     #pos = nx.random_layout(G)  # positions for all nodes


#     #networkx nodes
#     options = {"node_size": 500, "alpha": 0.8}
#     #G.add_nodes_from(G,nodelist=inter_neurons_nodes_list, node_color="r", **options)

#    # pprint(nodes_heirarchy)
#     for levels in range(0,len(nodes_heirarchy)):
#         nodes_in_level = nodes_heirarchy[levels][levels]
#         #pprint(nodes_in_level)
#         for node in nodes_in_level:
#             label =node.get('label')
#             pos = node.get('pos')
#             G.add_node(label, pos=pos)
        
#     # for k, v in motor_neuron_map.items():
#     #     label = v.get('label')
#     #     pos = v.get('pos')
#     #     G.add_node(label, pos=pos)
        
#     # #networkx edges
#     # for motor_index in range(0, inter2motor_col_length):
#     #     for inter_neuron_index in range(0,inter2motor_row_length): 
#     #         inter_neuron = inter_neuron_map[inter_neuron_index].get("label")
#     #         motor_neuron = motor_neuron_map[motor_index].get("label")
#     #         edge_weight = inter2motor_adj_weights[inter_neuron_index][motor_index]
#     #         edge_sign = '+' if edge_weight >=0 else '-'
#     #         edge_color = 'b' if edge_sign == '+' else "g"
#     #         abs_edge_weight = abs(edge_weight)
#     #         print(inter_neuron, motor_neuron, edge_weight, edge_sign, edge_color)
#     #         G.add_edge(inter_neuron,motor_neuron,color=edge_color, weight=abs_edge_weight, alpha=0.5)
        

#     values= []
#     # for node in G.nodes():
#     #     for key, value in inter_neuron_map.items():
#     #         label = value['label'] if 'label' in value else None
#     #         sign = value['sign'] if 'sign' in value else None
#     #         if(node == label):
#     #             values.append(get_node_color(node_dict=value))

#         # for key, value in motor_neuron_map.items():
#         #     label = value['label'] if 'label' in value else None 
#         #     sign = value['sign'] if 'sign' in value else None
#         #     if(node == label):
#         #         values.append(get_node_color(node_dict=value))

#     for node in G.nodes():
#         values.append(1)
    
#     node_colors= nx.get_node_attributes(G,'color').values()
#     node_pos= nx.get_node_attributes(G,'pos')
#     # edge_colors = nx.get_edge_attributes(G,'color').values()
#     # edge_weights = nx.get_edge_attributes(G,'weight').values()

#     #nx.draw(G, pos=node_pos, node_color=values,cmap=plt.cm.Reds,edge_color= edge_colors,width= list(edge_weights), with_labels=True)
#     nx.draw(G, pos=node_pos, node_color=values, cmap=plt.cm.Reds, with_labels=True)
#     plt.show()
