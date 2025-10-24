"""
DBSCAN Crime Spots Analysis - Main Entry Point

A streamlit app for analyzing san francisco crime data using dbscan clustering
"""

import streamlit as st

from src.config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT, CUSTOM_CSS
from src.data.loader import load_crime_data
from src.utils.ui_helpers import create_sidebar_navigation
from src.pages.home import render_home_page
from src.pages.theory import render_theory_page
from src.pages.dataset_overview import render_dataset_overview_page
from src.pages.data_visualization import render_data_visualization_page
from src.pages.dbscan_clustering import render_dbscan_clustering_page
from src.pages.interactive_maps import render_interactive_maps_page
from src.pages.heat_maps import render_heat_maps_page
from src.pages.summary import render_summary_page


def configure_page():
    """configure streamlit page settings"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_footer():
    """render app footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>DBSCAN Crime Spots Analysis | San Francisco Police Department Data 2016</p>
        <p>Built with Streamlit, Scikit-learn, Folium, and Pandas</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """main application entry point"""
    # setup page config
    configure_page()
    
    # load data
    with st.spinner("Loading data..."):
        df = load_crime_data()
    
    # create navigation
    page = create_sidebar_navigation()
    
    # route to appropriate page
    page_routes = {
        "🏠 Home": lambda: render_home_page(df),
        "📚 DBSCAN Theory": render_theory_page,
        "📊 Dataset Overview": lambda: render_dataset_overview_page(df),
        "📈 Data Visualization": lambda: render_data_visualization_page(df),
        "🎯 DBSCAN Clustering": lambda: render_dbscan_clustering_page(df),
        "🗺️ Interactive Maps": lambda: render_interactive_maps_page(df),
        "🔥 Heat Maps": lambda: render_heat_maps_page(df),
        "📑 Summary": lambda: render_summary_page(df)
    }
    
    # render selected page
    page_routes[page]()
    
    # render footer
    render_footer()


if __name__ == "__main__":
    main()
