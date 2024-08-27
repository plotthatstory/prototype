import streamlit as st

def render_component(component, layout):
    if component["type"] == "component":
        layout.write(component["name"])

def parse_layout(config, layout=None):
    if layout is None:
        layout = st.container()

    for item in config:
        item_type = item["type"]

        if item_type == "row":
            no_of_children = len(item.get("children", []))
            row = layout.columns(no_of_children)
            for i, child in enumerate(item["children"]):
                parse_layout([child], layout=row[i])

        elif item_type == "column":
            col = layout.container()
            for child in item["children"]:
                parse_layout([child], layout=col)

        else:
            render_component(item, layout)

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

# Render the layout
parse_layout(config)
