"""
interactive maps page - various folium map visualizations
"""

import streamlit as st
from streamlit_folium import st_folium

from src.utils.ui_helpers import render_section_header
from src.models.dbscan_model import run_dbscan
from src.data.processor import get_cluster_centers
from src.visualization.maps import (
    create_cluster_center_map, create_circle_marker_map,
    create_marker_cluster_map, create_combined_map
)
from src.config.settings import DEFAULT_EPS, DEFAULT_MIN_SAMPLES


def render_interactive_maps_page(df):
    """render the interactive maps page"""
    render_section_header("Interactive Map Visualizations")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Cluster Centers", 
        "Crime Markers", 
        "Marker Clusters",
        "Combined View"
    ])
    
    # run dbscan for maps
    sample_size = min(50000, len(df))
    df_sample = df.sample(n=sample_size, random_state=42).copy()
    
    with st.spinner("Preparing map data..."):
        labels, n_clusters, n_noise, df_SF = run_dbscan(
            df_sample, DEFAULT_EPS, DEFAULT_MIN_SAMPLES
        )
    
    mean_location_clusters, df_filtered = get_cluster_centers(df_sample, labels)
    
    with tab1:
        _render_cluster_centers_tab(mean_location_clusters, df_filtered)
    
    with tab2:
        _render_crime_markers_tab(df_sample)
    
    with tab3:
        _render_marker_clusters_tab(df_sample)
    
    with tab4:
        _render_combined_view_tab(mean_location_clusters, df_filtered, df_sample)


def _render_cluster_centers_tab(mean_location_clusters, df_filtered):
    """render cluster centers map"""
    st.markdown("### DBSCAN Cluster Centers")
    st.markdown("""
    This map shows the center points of identified crime clusters. Each marker represents
    a high-density crime area.
    """)
    
    sf_map = create_cluster_center_map(mean_location_clusters, df_filtered)
    st_folium(sf_map, width=1200, height=600)
    
    st.info(f"🎯 Showing {len(mean_location_clusters)} cluster centers")


def _render_crime_markers_tab(df_sample):
    """render individual crime markers"""
    st.markdown("### Individual Crime Markers")
    st.markdown("""
    Shows individual crime incidents as circle markers. Click on markers to see crime category.
    Limited to first 1000 incidents for performance.
    """)
    
    limit = st.slider("Number of incidents to display", 100, 2000, 1000, 100)
    
    sf_map = create_circle_marker_map(df_sample, limit)
    st_folium(sf_map, width=1200, height=600)
    
    st.info(f"📍 Displaying {min(limit, len(df_sample)):,} crime markers")


def _render_marker_clusters_tab(df_sample):
    """render marker clustering visualization"""
    st.markdown("### Marker Clustering")
    st.markdown("""
    Incidents are grouped into clusters for better visualization. Zoom in to see individual 
    markers. Numbers indicate how many incidents are in each cluster.
    """)
    
    limit = st.slider("Number of incidents for clustering", 500, 5000, 2000, 500)
    
    sf_map = create_marker_cluster_map(df_sample, limit)
    st_folium(sf_map, width=1200, height=600)
    
    st.info(f"🗂️ Clustering {min(limit, len(df_sample)):,} incidents")


def _render_combined_view_tab(mean_location_clusters, df_filtered, df_sample):
    """render combined view with clusters and points"""
    st.markdown("### Combined View: Clusters + Crime Points")
    st.markdown("""
    This map combines cluster centers (red markers) with individual crime incidents 
    (blue circles) for a comprehensive view.
    """)
    
    sf_map = create_combined_map(mean_location_clusters, df_filtered, df_sample)
    st_folium(sf_map, width=1200, height=600)
    
    st.info(f"🗺️ Showing {len(mean_location_clusters)} clusters and 500 crime points")

