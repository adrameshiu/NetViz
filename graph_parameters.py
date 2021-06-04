import pandas as pd
import numpy as np
import math


# Using the levels of each section of nodes, and the height and width from settings, find the position of each
# node in terms of x and y co ordinates and add them to the 'pos' key of each node The middle section will be
# centered at y=0 and the layers above and below will be incremented by the height parameter The middle node of each
# section will be centered at x=0 and the nodes to the left and right will be incremented by the width parameter ##
def get_node_positions(nodes_hierarchy, network_depth, height=10, width=10):
    origin_level = math.floor(network_depth / 2)
    for h in range(0, len(nodes_hierarchy)):
        level = nodes_hierarchy[h][h]
        y_pos = (origin_level - h) * height
        mid_level = math.floor(len(level) / 2)
        for w in range(0, len(level)):
            x_pos = math.floor((w - mid_level)) + width
            level[w]["pos"] = (x_pos, y_pos)
    return nodes_hierarchy


# Use the 'datafiles/edge_files.json' to find the path to the *.dat files
# that contain the path to the edges defined along with their from and to sections they connect.
def get_weights_from_file(edge_files_list, all_nodes):
    all_labels = [node['label'] for node in all_nodes]
    complete_adjacency_matrix = pd.DataFrame(columns=all_labels, index=all_labels)

    for edge_section in edge_files_list:
        file_path = edge_section['path']
        from_section_label = edge_section['columns_section']
        to_section_label = edge_section['rows_section']

        from_nodes_labels = [node['label'] for node in all_nodes if node['type'] == from_section_label]
        to_nodes_labels = [node['label'] for node in all_nodes if node['type'] == to_section_label]

        file_adj_weights = np.loadtxt(file_path, dtype=float)
        file_df = pd.DataFrame(file_adj_weights, columns=from_nodes_labels, index=to_nodes_labels)

        for from_node in from_nodes_labels:
            for to_node in to_nodes_labels:
                complete_adjacency_matrix.loc[to_node, from_node] = file_df.loc[to_node, from_node]

    return complete_adjacency_matrix
