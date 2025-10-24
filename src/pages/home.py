"""
home page - welcome screen with overview and quick stats
"""

import streamlit as st
from src.utils.ui_helpers import render_header


def render_home_page(df):
    """render the home/welcome page"""
    render_header("🚨 DBSCAN Algorithm for Crime Spot Detection")
    st.markdown("### Analyzing San Francisco Crime Data with Density-Based Clustering")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### About This Application
        
        This interactive application demonstrates the **DBSCAN (Density-Based Spatial Clustering of 
        Applications with Noise)** algorithm applied to real-world crime data from San Francisco. 
        
        #### Features:
        - 📊 **Dataset Exploration**: Interactive exploration of 150,500+ crime incidents
        - 📚 **Educational Content**: Learn how DBSCAN algorithm works
        - 🎯 **Interactive Clustering**: Adjust parameters and see results in real-time
        - 🗺️ **Advanced Visualizations**: Multiple map types (choropleth, markers, clusters, heatmaps)
        - 📈 **Statistical Analysis**: Detailed insights into crime patterns
        
        #### Dataset Information:
        The dataset contains crime incidents from San Francisco police department with information about:
        - Crime categories and descriptions
        - Geographic coordinates (latitude/longitude)
        - Time and date of incidents
        - Police district information
        - Resolution status
        
        **Use the sidebar to navigate through different sections!**
        """)
    
    with col2:
        st.info("**Quick Stats**")
        st.metric("Total Incidents", f"{len(df):,}")
        st.metric("Crime Categories", df['Category'].nunique())
        st.metric("Police Districts", df['PdDistrict'].nunique())
        st.metric("Time Period", "2016")
        
        st.success("✅ Data loaded successfully!")

