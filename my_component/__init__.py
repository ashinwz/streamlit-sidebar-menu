import streamlit as st
import streamlit.components.v1 as components

import os

_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://10.86.96.31:3002",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "my_component", path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def my_component(menu_title, name, options, icons=None, key=None,  default_index=0):
    component_value = _component_func(name=name, key=key, default=options[default_index], menuTitle=menu_title, options=options, defaultIndex=default_index, icons=icons)
    return component_value

def intro():
    st.markdown("### intro")

def upload():
    st.markdown("### upload")

def run():
    st.markdown("## run")

st.set_page_config(page_title="demo", layout="wide")

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True) # Load the on hover side bar css file

# Create an instance of our component with a constant `name` arg, and
# print its output value.
if 'selected' not in st.session_state:
  st.session_state.selected = "Introduction"
  st.session_state.toggle = True

with st.sidebar:
    selected = my_component("AutoCell","World", ["Introduction","Data Upload",'Run'], default_index=0, icons=['bx-home-alt', 'bx-bar-chart-alt-2', 'bx-bell'])

if type(selected) == type(1):
    if selected %2 != 0:
        st.markdown(
            """
            <style>
                section[data-testid='stSidebar'] > div:nth-of-type(1) {
                    width: 5vh;
                    transition: all 0.5s ease;
                }
            </style>
            """
        , unsafe_allow_html=True)
        
        st.session_state.toggle = False
    else:
        st.session_state.toggle = True

    selected = st.session_state.selected

elif type(selected) == type('string'):
    st.session_state.selected = selected
    if st.session_state.toggle == False:
        st.markdown(
            """
            <style>
                section[data-testid='stSidebar'] > div:nth-of-type(1) {
                    width: 5vh;
                    transition: all 0.5s ease;
                }
            </style>
            """
        , unsafe_allow_html=True)


page_names_to_funcs = {
    "Introduction":   {"fn": intro},
    "Data Upload":    {"fn": upload},
    "Run":            {"fn": run}
}

print(selected)

if selected in page_names_to_funcs.keys():
    page_names_to_funcs[selected]["fn"]()


# if new_num_clicks == st.session_state.value + 1 :
#     # st.markdown("Change, You've clicked %s times!" % int(new_num_clicks))
#     st.session_state.value  = new_num_clicks
#     if new_num_clicks %2 !=0:
#         st.markdown(
#             """
#             <style>
#                 section[data-testid='stSidebar'] > div:nth-of-type(1) {
#                     width: 5vh;
#                     transition: all 0.5s ease;
#                 }
#             </style>
#             """
#         , unsafe_allow_html=True)
#     else:
#         pass