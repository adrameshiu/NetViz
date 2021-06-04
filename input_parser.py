import matplotlib.pyplot as plt


# Parse the nodes json under 'datafiles/nodes.json'
# that contains information of the level name and nodes in each level
def parse_nodes_json(nodes_json):
    level = 0
    network_depth = len(nodes_json)
    nodes_hierarchy = []
    all_nodes = []

    for node_category_json in nodes_json:
        nodes = []
        node_type = node_category_json.get("name")
        nodes_in_category = node_category_json.get("nodes")
        for node in nodes_in_category:
            node_dict = {"label": node, "level": level, "type": node_type, "node_index": (len(all_nodes) + 1)}
            nodes.append(node_dict)
            all_nodes.append(node_dict)

        nodes_hierarchy.append({level: nodes})
        level = level + 1
    return nodes_hierarchy, all_nodes, network_depth


# Parse the options json under 'settings/options.json'
# that contains information about the different setting options like height and width between
# two nodes
def parse_options_json(options_json):
    node_cmap = options_json["node_cmap"] if "node_cmap" in options_json else plt.cm.Greens  # setting default value
    edge_cmap = options_json["edge_cmap"] if "edge_cmap" in options_json else plt.cm.Set2
    height = options_json["height"] if "height" in options_json else None
    width = options_json["width"] if "width" in options_json else None

    return node_cmap, edge_cmap, height, width
