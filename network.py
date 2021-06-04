import json
import input_parser
import graph_parameters
import build_network


def main():
    with open('datafiles/nodes.json') as json_file:
        node_def = json.load(json_file)

    with open('datafiles/edge_files.json') as json_file:
        edge_files_list = json.load(json_file)

    with open('settings/options.json') as json_file:
        options_json = json.load(json_file)

    nodes_hierarchy, all_nodes, network_depth = input_parser.parse_nodes_json(node_def)
    node_cmap, edge_cmap, height, width = input_parser.parse_options_json(options_json)

    complete_adjacency_matrix = graph_parameters.get_weights_from_file(edge_files_list, all_nodes)
    network_inputs = (
        nodes_hierarchy, all_nodes, network_depth, complete_adjacency_matrix, height, width, node_cmap, edge_cmap)
    build_network.build_network(*network_inputs)


if __name__ == "__main__":
    main()
