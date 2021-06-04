import graph_parameters
import networkx as nx
import math
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json


def build_network(nodes_hierarchy, all_nodes, network_depth,
                  complete_adjacency_matrix,
                  height, width,
                  node_cmap, edge_cmap):
    positive_sign_color = '#add8e6'
    negative_sign_color = '#ff80ff'
    node_color = '#C0C0C0'

    nodes_hierarchy = graph_parameters.get_node_positions(nodes_hierarchy=nodes_hierarchy, network_depth=network_depth,
                                                          height=height,
                                                          width=width)

    G = nx.Graph()

    for node in all_nodes:
        label = node.get('label')
        pos = node.get('pos')
        G.add_node(label, pos=pos)

    node_color_values = []
    for node in G.nodes():
        node_color_values.append(node_color)  # color scale value for nodes set to max

    node_pos = nx.get_node_attributes(G, 'pos')

    for node1 in all_nodes:
        for node2 in all_nodes:
            node1_label = node1.get("label")
            node2_label = node2.get("label")
            edge_weight = complete_adjacency_matrix.loc[node1_label, node2_label]
            if not math.isnan(edge_weight):  # if there is a value in the complete adj matrix for the edge
                edge_sign = '+' if edge_weight >= 0 else '-'
                edge_color = positive_sign_color if edge_sign == '+' else negative_sign_color
                # edge_color = 0.8 if edge_sign == '+' else 1
                abs_edge_weight = abs(edge_weight)
                G.add_edge(node1_label, node2_label, color=edge_color, weight=abs_edge_weight, alpha=0.5)

    edge_colors = nx.get_edge_attributes(G, 'color').values()
    edge_weights = nx.get_edge_attributes(G, 'weight').values()

    plt.figure("Overall Hierarchy")

    nx.draw(G, pos=node_pos, node_color=node_color_values, cmap=node_cmap, edge_cmap=edge_cmap, edge_color=edge_colors,
            width=list(edge_weights), with_labels=True)

    # converting to set to get unique values of levels and then converting it back to list of all unique levels
    all_levels = list(set([node['level'] for node in all_nodes]))

    # a separate graph for interneurons
    for level in all_levels:
        has_same_level_graphs = False
        all_nodes_in_level = [node['label'] for node in all_nodes if node['level'] == level]
        for node1 in all_nodes_in_level:
            for node2 in all_nodes_in_level:
                edge_weight = complete_adjacency_matrix.loc[node1, node2]
                if not math.isnan(edge_weight):
                    if not has_same_level_graphs:
                        sub_G = nx.DiGraph()
                        has_same_level_graphs = True

                    edge_sign = '+' if edge_weight >= 0 else '-'
                    edge_color = positive_sign_color if edge_sign == '+' else negative_sign_color
                    # edge_color = 0.8 if edge_sign == '+' else 1
                    abs_edge_weight = abs(edge_weight)
                    sub_G.add_edge(node1, node2, color=edge_color, weight=abs_edge_weight, alpha=0.5,
                                   edge_type='chemical')

        if has_same_level_graphs:
            draw_graph_within_level(G=sub_G, node_color=node_color,
                                    node_cmap=node_cmap, edge_cmap=edge_cmap)

    plt.show()


def draw_graph_within_level(G, node_color, node_cmap, edge_cmap):
    node_color_values = []
    for node in G.nodes():
        node_color_values.append(node_color)  # color scale value for nodes set to max

    node_colors = nx.get_node_attributes(G, 'color').values()

    node_pos = nx.get_node_attributes(G, 'pos')
    edge_colors = nx.get_edge_attributes(G, 'color').values()
    edge_weights = nx.get_edge_attributes(G, 'weight').values()
    edge_types = nx.get_edge_attributes(G, 'edge_type')
    sub_pos = nx.circular_layout(G)
    plt.figure("Inter-neurons")
    nx.draw(G, sub_pos, node_color=node_color_values, cmap=node_cmap, edge_cmap=edge_cmap,
            edge_color=edge_colors, width=list(edge_weights), connectionstyle='arc3, rad = 0.1',
            with_labels=True)

    nx.draw_networkx_edge_labels(G, sub_pos, edge_labels=edge_types)


def find_self_loops(G):
    return list(nx.selfloop_edges(G, keys=True, data=True))


def generate_json_dump(G):
    data = json_graph.node_link_data(G)
    with open('graph_out.json', 'w') as f:
        json.dump(data, f, indent=4)
