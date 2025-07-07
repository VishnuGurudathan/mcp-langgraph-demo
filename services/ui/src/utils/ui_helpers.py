# ui/src/utils/ui_helpers.py

import streamlit as st

def inject_custom_css() -> None:
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        height: 100%;
        overflow: hidden;
    }

    .main .block-container {
        padding-top: 100px !important;  /* Push below header */
        padding-bottom: 80px !important;  /* For footer space */
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        padding: 1rem 2rem 0.5rem 2rem;
        background-color: #0e1117;
        border-bottom: 1px solid #333;
        text-align: center;
    }

    .header-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }

    .header-subtitle {
        font-size: 1.1rem;
        margin-top: 0;
        color: #bbb;
    }

    .scrollable-chat-container {
        position: absolute;
        top: 100px;
        bottom: 80px;
        overflow-y: auto;
        width: 100%;
        padding: 0 1rem;
    }

    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        padding: 1rem 2rem;
        background-color: #0e1117;
        border-top: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

