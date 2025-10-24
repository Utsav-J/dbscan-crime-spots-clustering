"""
dbscan clustering implementation for crime spot detection
"""

import streamlit as st
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler


@st.cache_data
def run_dbscan(df, eps, min_samples):
    """
    run dbscan clustering on crime location data
    
    returns labels, number of clusters, noise count, and coordinates
    """
    df_SF = df[['X', 'Y']].copy()
    
    # normalize coordinates to 0-1 range
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df_SF)
    
    # apply dbscan
    crime_points = DBSCAN(eps=eps, min_samples=min_samples).fit(df_scaled)
    labels = crime_points.labels_
    
    # calculate stats
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    return labels, n_clusters, n_noise, df_SF


def get_clustering_metrics(labels, total_points):
    """calculate clustering quality metrics"""
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    clustered_points = total_points - n_noise
    noise_percentage = (n_noise / total_points) * 100
    clustered_percentage = (clustered_points / total_points) * 100
    
    return {
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'clustered_points': clustered_points,
        'noise_percentage': noise_percentage,
        'clustered_percentage': clustered_percentage
    }

