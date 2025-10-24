"""
heat maps page - density-based crime visualization
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from src.utils.ui_helpers import render_section_header
from src.visualization.maps import create_heat_map


def render_heat_maps_page(df):
    """render the heat maps page"""
    render_section_header("Heat Map Analysis")
    
    st.markdown("""
    Heat maps provide an intuitive visualization of crime density across San Francisco.
    Brighter/redder areas indicate higher concentrations of criminal activity.
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### Settings")
        sample_size = st.slider(
            "Sample Size",
            1000, 20000, 10000, 1000,
            help="Number of incidents to include in heat map"
        )
        
        radius = st.slider(
            "Heat Radius",
            10, 50, 15,
            help="Size of heat spots"
        )
        
        blur = st.slider(
            "Blur Amount",
            10, 40, 15,
            help="Amount of blur for heat spots"
        )
        
        max_intensity = st.slider(
            "Max Intensity",
            1, 10, 5,
            help="Maximum heat intensity"
        )
    
    with col1:
        # create heat map
        df_heat = df.sample(n=min(sample_size, len(df)), random_state=42)
        sf_heat_map = create_heat_map(df_heat, radius, blur, max_intensity)
        st_folium(sf_heat_map, width=900, height=600)
    
    st.info(f"🔥 Heat map generated from {len(df_heat):,} incidents")
    
    # additional analysis
    st.markdown("### Heat Map Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Incidents Analyzed", f"{len(df_heat):,}")
    
    with col2:
        # find the area with most crimes (approximate)
        lat_bins = pd.cut(df_heat['Y'], bins=10)
        lon_bins = pd.cut(df_heat['X'], bins=10)
        grid_counts = df_heat.groupby([lat_bins, lon_bins]).size()
        max_grid = grid_counts.max()
        st.metric("Max Density Grid", f"{max_grid} crimes")
    
    with col3:
        avg_crimes = len(df_heat) / 100  # approximate grid cells
        st.metric("Avg per Area", f"{avg_crimes:.0f}")
    
    st.markdown("""
    #### Understanding Heat Maps
    
    - **Red/Bright areas**: High concentration of crimes (hotspots)
    - **Yellow/Orange areas**: Moderate crime activity
    - **Blue/Dark areas**: Low crime activity
    - **No color**: Minimal to no reported incidents
    
    Use the sliders to adjust visualization parameters and explore different perspectives of the data.
    """)

