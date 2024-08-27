import streamlit as st
import networkx as nx
import plotly.graph_objs as go

def add_edges_from_component(graph, component):
    for downstream in component.get("downstream", []):
        graph.add_edge(component["id"], downstream)
    for upstream in component.get("upstream", []):
        graph.add_edge(upstream, component["id"])

def parse_layout(config, layout=None, component_list=None):
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
                "type": item["component_type"],
                "options": item.get("args", {}),
                "upstream": item.get("upstream", []),
                "downstream": item.get("downstream", []),
                "component_value": None,
                "layout": layout
            })

    return component_list

def render_components(component_list):
    component_list.sort(key=lambda x: x.get("render_order", 0))

    for component in component_list:
        layout = component["layout"]
        options = component["options"]
        component_type = component["type"]

        if component_type == "slider":
            component["component_value"] = layout.slider(label=component["id"], **options)
        elif component_type == "button":
            if layout.button(label=options.get("label", "Button")):
                component["component_value"] = True
            else:
                component["component_value"] = False
        elif component_type == "plotly_chart":
            fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[1, 3, 2]))
            layout.plotly_chart(fig)
            component["component_value"] = fig
        else:
            layout.text(f"Unknown component: {component_type}")

# Initialize graph
G = nx.DiGraph()


config = [
    {"type": "row", "children": [
        {"type": "row", "children": [
            {"type": "component", "name": "Slider A", "component_type": "slider", "args": {"min_value": 0, "max_value": 100, "value": 50}, "upstream": [], "downstream": ["Chart C", "Component D"]},
            {"type": "component", "name": "Button E", "component_type": "button", "args": {"label": "Click Me"}, "upstream": [], "downstream": []}
        ]},
        {"type": "column", "children": [
            {"type": "component", "name": "Range B", "component_type": "slider", "args": {"min_value": 0, "max_value": 50, "value": (10, 40)}, "upstream": [], "downstream": ["Component D"]},
            {"type": "component", "name": "Chart C", "component_type": "plotly_chart", "args": {"data": {}}, "upstream": ["Slider A"], "downstream": ["Component D"]}
        ]}
    ]},
    {"type": "row", "children": [
        {"type": "column", "children": [
            {"type": "component", "name": "Component D", "component_type": "plotly_chart", "args": {"data": {}}, "upstream": ["Slider A", "Range B", "Chart C"], "downstream": []}
        ]}
    ]}
]

# config = [
#     {"type": "row", "children": [
#         {"type": "component", "name": "Select Species", "component_type": "select", "args": {"options": ["setosa", "versicolor", "virginica"], "label": "Select Species"}, "upstream": [], "downstream": ["Range Filter"]},
#         {"type": "component", "name": "Range Filter", "component_type": "slider", "args": {"min_value": 0, "max_value": 10, "value": (0, 10), "label": "Petal Width Range"}, "upstream": ["Select Species"], "downstream": ["Scatter Chart"]}
#     ]},
#     {"type": "row", "children": [
#         {"type": "component", "name": "Scatter Chart", "component_type": "plotly_chart", "args": {"data": {}, "title": "Scatter Plot"}, "upstream": ["Range Filter"], "downstream": []}
#     ]}
# ]

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
