# import plotly.express as px
# import streamlit as st

# # from plotly1 import plotly_events
# from plotly2 import plotly_events
# # from plotly3 import plotly_events

# df = px.data.iris()
# fig = px.scatter(df, x="sepal_width", y="sepal_length", title="Sample Figure")

# value = plotly_events(fig)
# st.write("Received", value)

import streamlit as st
from lit1 import st_my_button

st.title("Custom Lit Button in Streamlit")

# # Use the custom button component
result = st_my_button()

# # Display the result
if result:
    st.write(result)

# st.markdown("""<style> .my-button:has(iframe[height="0"]) {display: block; } </style> """,unsafe_allow_html=True)

# Render the Lit component
# st.components.v1.html(
#     "<my-button></my-button>",
#     height=100,  # Set height according to your component's needs
#     width=200,   # Set width according to your component's needs
#     scrolling=True
# )


# import streamlit as st
# import streamlit.components.v1 as components