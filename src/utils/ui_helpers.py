"""
helper functions for streamlit ui components
"""

import streamlit as st


def render_header(text, css_class="main-header"):
    """render a styled header"""
    st.markdown(f'<h1 class="{css_class}">{text}</h1>', unsafe_allow_html=True)


def render_section_header(text):
    """render a section header"""
    st.markdown(f'<h2 class="section-header">{text}</h2>', unsafe_allow_html=True)


def render_metrics_row(metrics_dict):
    """render a row of metrics"""
    cols = st.columns(len(metrics_dict))
    for col, (label, value) in zip(cols, metrics_dict.items()):
        col.metric(label, value)


def create_sidebar_navigation():
    """create sidebar navigation menu"""
    st.sidebar.title("Navigation")
    return st.sidebar.radio(
        "Go to",
        ["🏠 Home", "📚 DBSCAN Theory", "📊 Dataset Overview", 
         "📈 Data Visualization", "🎯 DBSCAN Clustering", 
         "🗺️ Interactive Maps", "🔥 Heat Maps", "📑 Summary"]
    )


def display_feature_info():
    """display dataset feature descriptions"""
    feature_info = {
        "IncidntNum": "Unique incident number identifier",
        "Category": "Category of crime or incident",
        "Descript": "Detailed description of the crime",
        "DayOfWeek": "Day of week when incident occurred",
        "Date": "Date of the incident",
        "Time": "Time of day when incident occurred",
        "PdDistrict": "Police department district",
        "Resolution": "How the crime was resolved",
        "Address": "Closest address to incident location",
        "X": "Longitude coordinate",
        "Y": "Latitude coordinate",
        "Location": "Tuple of latitude and longitude",
        "PdId": "Police department ID"
    }
    return feature_info

