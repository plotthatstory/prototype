import streamlit as st
import networkx as nx

def add_edges_from_component(graph, component):
    """Add edges to the graph based on the component's upstream and downstream dependencies."""
    for downstream in component.get("downstream", []):
        graph.add_edge(component["id"], downstream)
    for upstream in component.get("upstream", []):
        graph.add_edge(upstream, component["id"])

def parse_layout(config, layout=None, component_list=None):
    """Recursively parse the config and build the component list and layout structure."""
    if component_list is None:
        component_list = []
    if layout is None:
        layout = st.container()

    for item in config:
        item_type = item["type"]

        if item_type == "row":
            no_of_children = len(item.get("children", []))
            row = layout.columns(no_of_children)
            for i, child in enumerate(item["children"]):
                parse_layout([child], layout=row[i], component_list=component_list)

        elif item_type == "column":
            col = layout.container()
            for child in item["children"]:
                parse_layout([child], layout=col, component_list=component_list)

        elif item_type == "component":
            component_list.append({
                "id": item["name"],
                "type": item_type,
                "options": {},  # Add any specific options here
                "upstream": item.get("upstream", []),
                "downstream": item.get("downstream", []),
                "component_value": None,
                "layout": layout
            })

    return component_list

def render_components(component_list):
    """Render the components based on their type and layout."""
    # Sort components by render order
    component_list.sort(key=lambda x: x.get("render_order", 0))

    # Render components in order
    for component in component_list:
        layout = component["layout"]
        if component["id"].startswith("Component"):
            # Simulate the component by rendering its name
            component["component_value"] = layout.text(component["id"])

# Example config
config = [
    {"type": "row", "children": [
        {"type": "row", "children": [
            {"type": "component", "name": "Component A", "upstream": [], "downstream": ["Component C", "Component D"]},
            {"type": "component", "name": "Component E", "upstream": [], "downstream": []}
        ]},
        {"type": "column", "children": [
            {"type": "component", "name": "Component B", "upstream": [], "downstream": ["Component D"]},
            {"type": "component", "name": "Component C", "upstream": ["Component A"], "downstream": ["Component D"]}
        ]}
    ]},
    {"type": "row", "children": [
        {"type": "column", "children": [
            {"type": "component", "name": "Component D", "upstream": ["Component A", "Component B", "Component C"], "downstream": []}
        ]}
    ]}
]

# Initialize graph
G = nx.DiGraph()

# Parse config to generate component list and layout
component_list = parse_layout(config)

# Build the dependency graph
for component in component_list:
    add_edges_from_component(G, component)

# Determine the render order based on topological sort
sorted_components = list(nx.topological_sort(G))

# Update component list with render order
for index, component_name in enumerate(sorted_components):
    for component in component_list:
        if component["id"] == component_name:
            component["render_order"] = index + 1
            break

# Render components
render_components(component_list)
