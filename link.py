import streamlit as st
import plotly.express as px
import pandas as pd
import networkx as nx

# Load Iris dataset
@st.cache
def load_iris_data():
    df = px.data.iris()
    return df

df = load_iris_data()

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
    component_dict = {component["id"]: component for component in component_list}
    
    for component in component_list:
        layout = component["layout"]
        options = component["options"]
        component_type = component["type"]

        if component_type == "selectbox":
            component["component_value"] = layout.selectbox(**options)
        elif component_type == "slider":
            component["component_value"] = layout.slider(**options)
        elif component_type == "plotly_chart":
            selected_species = component_dict["Select Species"]["component_value"]
            min_width, max_width = component_dict["Range Filter"]["component_value"]
            filtered_df = df[df['species'] == selected_species]
            filtered_df = filtered_df[(filtered_df['petal_width'] >= min_width) & (filtered_df['petal_width'] <= max_width)]
            fig = px.scatter(filtered_df, x="sepal_width", y="sepal_length", color="species", title=options["title"])
            layout.plotly_chart(fig)
        else:
            layout.text(f"Unknown component: {component_type}")

# Initialize graph
G = nx.DiGraph()

config = [
    {"type": "row", "children": [
        {"type": "component", "name": "Select Species", "component_type": "selectbox", "args": {"options": ["setosa", "versicolor", "virginica"], "label": "Select Species"}, "upstream": [], "downstream": ["Range Filter"]},
        {"type": "component", "name": "Range Filter", "component_type": "slider", "args": {"min_value": 0, "max_value": 10, "value": (0, 10), "label": "Petal Width Range"}, "upstream": ["Select Species"], "downstream": ["Scatter Chart"]}
    ]},
    {"type": "row", "children": [
        {"type": "component", "name": "Scatter Chart", "component_type": "plotly_chart", "args": {"data": {}, "title": "Scatter Plot"}, "upstream": ["Range Filter"], "downstream": []}
    ]}
]


# Parse config to generate component list and layout
component_list = parse_layout(config)

# Build the dependency graph
def add_edges_from_component(graph, component):
    for downstream in component.get("downstream", []):
        graph.add_edge(component["id"], downstream)
    for upstream in component.get("upstream", []):
        graph.add_edge(upstream, component["id"])

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
