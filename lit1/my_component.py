import os
import streamlit.components.v1 as components

_USE_WEB_DEV_SERVER = False

if _USE_WEB_DEV_SERVER:
    _component_func = components.declare_component(
        "my_button", url="http://localhost:1234"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_button", path=build_dir)

def st_my_button():
    component_value = _component_func()
    return component_value
