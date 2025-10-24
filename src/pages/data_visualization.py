"""
data visualization page - scatter plots and choropleth maps
"""

import streamlit as st
from streamlit_folium import st_folium

from src.utils.ui_helpers import render_section_header
from src.data.loader import load_geojson
from src.data.processor import prepare_district_data
from src.visualization.plots import plot_crime_scatter, plot_district_bar_chart
from src.visualization.maps import create_choropleth_map


def render_data_visualization_page(df):
    """render the data visualization page"""
    render_section_header("Data Visualization")
    
    tab1, tab2 = st.tabs(["Scatter Plots", "Choropleth Map"])
    
    with tab1:
        _render_scatter_tab(df)
    
    with tab2:
        _render_choropleth_tab(df)


def _render_scatter_tab(df):
    """render scatter plot visualization"""
    st.markdown("### Crime Location Distribution")
    st.markdown("""
    This scatter plot shows the geographic distribution of all crime incidents in San Francisco.
    The X-axis represents longitude and Y-axis represents latitude. High-density areas indicate
    crime hotspots.
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        plot_size = st.slider("Plot Size", 8, 16, 12)
        alpha_value = st.slider("Point Transparency", 0.1, 1.0, 0.35)
        sample_size = st.slider("Sample Size (for performance)", 1000, len(df), 
                               min(50000, len(df)), step=1000)
    
    with col1:
        df_sample = df.sample(n=min(sample_size, len(df)), random_state=42)
        fig = plot_crime_scatter(df_sample, alpha=alpha_value, size=plot_size)
        st.pyplot(fig)
    
    st.info(f"📊 Displaying {len(df_sample):,} out of {len(df):,} incidents")


def _render_choropleth_tab(df):
    """render choropleth map"""
    st.markdown("### Crime Rate by District - Choropleth Map")
    st.markdown("""
    This choropleth map shows the crime intensity across different police districts in 
    San Francisco. Darker colors indicate higher crime rates.
    """)
    
    try:
        geojson_path, geojson_data = load_geojson()
        df_san = prepare_district_data(df)
        
        sanfran_map = create_choropleth_map(geojson_data, df_san)
        st_folium(sanfran_map, width=1200, height=600)
        
        st.markdown("#### District Statistics")
        df_san_sorted = df_san.sort_values('Count', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 5 Districts by Crime Count**")
            st.dataframe(df_san_sorted.head(), use_container_width=True)
        
        with col2:
            fig = plot_district_bar_chart(df_san_sorted)
            st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error loading choropleth map: {str(e)}")
        st.info("Showing district data in table format instead:")
        df_san = prepare_district_data(df)
        st.dataframe(df_san.sort_values('Count', ascending=False), 
                   use_container_width=True)

