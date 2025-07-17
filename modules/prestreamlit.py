import streamlit as st
from streamlit_js_eval import streamlit_js_eval as stjs

def getWindowSize() -> list:
    windows_width = stjs(js_expressions="window.innerWidth", key="WINDOW_WIDTH")
    windows_height = stjs(js_expressions="window.innerHeight", key="WINDOW_HEIGHT")
    print(windows_width," ", windows_height)
    return [windows_width, windows_height]

metadata_response = { # px
    "expanded-min-window-size": 1100,
    "collapsed-min-windows-size": 1356,
    "box-chart-block-size": 65,
    "block-size": 420,
    "sidebar-width": 256,
    "padding-block-width": 330
}

