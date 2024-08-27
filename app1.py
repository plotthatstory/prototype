import streamlit as st
import os
import uuid

st.title("Custom Lit Button in Streamlit")

# Use the iframe JS injection functions to fix the height issue
def inject_iframe_js_code(source: str) -> None:
    div_id = str(uuid.uuid4())  # Generate a unique ID for the div

    st.markdown(
        f"""
    <div style="height: 0; width: 0; overflow: hidden;" id="{div_id}">
        <iframe src="javascript: \
            var script = document.createElement('script'); \
            script.type = 'text/javascript'; \
            script.text = {html.escape(repr(source))}; \
            var div = window.parent.document.getElementById('{div_id}'); \
            div.appendChild(script); \
            setTimeout(function() {{ }}, 0); \
        "></iframe>
    </div>
    """,
        unsafe_allow_html=True,
    )

def js_show_zeroheight_iframe(component_iframe_title: str, height: int = 600):
    source = f"""
    (function() {{
        var attempts = 0;
        const maxAttempts = 20; // Max attempts to find the iframe
        const intervalMs = 1000; // Interval between attempts in milliseconds
        
        const intervalId = setInterval(function() {{
            var iframe = document.querySelector('iframe[title="{component_iframe_title}"]');
            if (iframe || attempts > maxAttempts) {{
                if (iframe) {{
                    iframe.style.height = "{height}px";
                    iframe.setAttribute("height", "{height}");
                    console.log('Height of iframe with title "{component_iframe_title}" set to {height}px.');
                }} else {{
                    console.log('Iframe with title "{component_iframe_title}" not found after ' + maxAttempts + ' attempts.');
                }}
                clearInterval(intervalId); // Stop checking
            }}
            attempts++;
        }}, intervalMs);
    }})();
    """

    inject_iframe_js_code(source)

# Render the custom component iframe
component_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lit Button Component</title>
    <script type="module" src="index.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
    <my-button></my-button>
</body>
</html>
"""

iframe_html = f"""
<iframe
    srcdoc="{component_html.replace('"', '&quot;')}"
    style="width: 100%; border: none; height: 300px;"
    id="lit-component-iframe"
    title="lit-button-component"
></iframe>
"""

st.components.v1.html(iframe_html, height=300)

# Adjust iframe height dynamically using the custom JS
js_show_zeroheight_iframe("lit-button-component", height=300)
