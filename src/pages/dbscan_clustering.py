"""
dbscan clustering page - interactive parameter tuning and cluster visualization
"""

import streamlit as st

from src.utils.ui_helpers import render_section_header
from src.models.dbscan_model import run_dbscan, get_clustering_metrics
from src.data.processor import calculate_cluster_stats, get_cluster_centers
from src.visualization.plots import (
    plot_clusters_with_noise, plot_clusters_without_noise,
    plot_cluster_sizes, plot_noise_distribution
)


def render_dbscan_clustering_page(df):
    """render the interactive dbscan clustering page"""
    render_section_header("DBSCAN Clustering Analysis")
    
    st.markdown("""
    Adjust the DBSCAN parameters below to see how they affect the clustering results.
    The algorithm will identify crime hotspots and classify outliers.
    """)
    
    # parameter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eps = st.slider(
            "Epsilon (ε) - Neighborhood Radius",
            min_value=0.001,
            max_value=0.050,
            value=0.020,
            step=0.001,
            help="Maximum distance between two samples to be considered neighbors"
        )
    
    with col2:
        min_samples = st.slider(
            "Min Samples - Minimum Points",
            min_value=50,
            max_value=1000,
            value=500,
            step=50,
            help="Minimum number of samples in a neighborhood for a point to be a core point"
        )
    
    with col3:
        sample_size = st.slider(
            "Sample Size (for performance)",
            min_value=10000,
            max_value=len(df),
            value=min(50000, len(df)),
            step=10000
        )
    
    # run dbscan
    df_sample = df.sample(n=min(sample_size, len(df)), random_state=42).copy()
    
    with st.spinner("Running DBSCAN algorithm..."):
        labels, n_clusters, n_noise, df_SF = run_dbscan(df_sample, eps, min_samples)
    
    df_sample['Cluster'] = labels
    
    # display results
    st.markdown("### Clustering Results")
    
    metrics = get_clustering_metrics(labels, len(df_sample))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clusters Found", metrics['n_clusters'])
    col2.metric("Noise Points", f"{metrics['n_noise']:,}")
    col3.metric("Clustered Points", f"{metrics['clustered_points']:,}")
    col4.metric("Noise Percentage", f"{metrics['noise_percentage']:.1f}%")
    
    # tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["With Noise", "Without Noise", "Cluster Details"])
    
    with tab1:
        _render_with_noise_tab(df_sample, labels)
    
    with tab2:
        _render_without_noise_tab(df_sample, labels, n_clusters)
    
    with tab3:
        _render_cluster_details_tab(df_sample, labels, n_clusters, n_noise)


def _render_with_noise_tab(df_sample, labels):
    """render clusters with noise points"""
    st.markdown("#### Crime Spots with Noise Points (Label = -1)")
    
    fig = plot_clusters_with_noise(df_sample, labels)
    st.pyplot(fig)


def _render_without_noise_tab(df_sample, labels, n_clusters):
    """render clusters without noise points"""
    st.markdown("#### Crime Spots without Noise Points")
    
    if n_clusters > 0:
        mean_location_clusters, df_filtered = get_cluster_centers(df_sample, labels)
        
        fig = plot_clusters_without_noise(df_filtered, mean_location_clusters)
        st.pyplot(fig)
        
        st.success(f"✅ Successfully identified {n_clusters} crime hotspot clusters!")
    else:
        st.warning("No clusters found with current parameters. Try adjusting eps or min_samples.")


def _render_cluster_details_tab(df_sample, labels, n_clusters, n_noise):
    """render detailed cluster information"""
    st.markdown("#### Detailed Cluster Information")
    
    if n_clusters > 0:
        cluster_df = calculate_cluster_stats(df_sample, labels)
        st.dataframe(cluster_df, use_container_width=True)
        
        # cluster visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            df_filtered = df_sample[df_sample['Cluster'] != -1].copy()
            fig = plot_cluster_sizes(df_filtered)
            st.pyplot(fig)
        
        with col2:
            n_clustered = len(df_sample) - n_noise
            fig = plot_noise_distribution(n_clustered, n_noise)
            st.pyplot(fig)
    else:
        st.warning("No clusters found. Try different parameters.")

