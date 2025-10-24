"""
data processing and transformation utilities
"""

import pandas as pd
import streamlit as st


@st.cache_data
def prepare_district_data(df):
    """aggregate crime counts by police district"""
    df_san = df[["PdDistrict", "Category"]].groupby("PdDistrict").count()
    df_san = df_san.reset_index()
    df_san.rename(columns={'PdDistrict': 'Neighborhood', 'Category': 'Count'}, inplace=True)
    return df_san


def filter_by_district(df, districts):
    """filter dataframe by police districts"""
    if districts:
        return df[df['PdDistrict'].isin(districts)]
    return df


def filter_by_category(df, categories):
    """filter dataframe by crime categories"""
    if categories:
        return df[df['Category'].isin(categories)]
    return df


def get_top_categories(df, n=10):
    """get top n crime categories by count"""
    return df['Category'].value_counts().head(n)


def get_district_counts(df):
    """get crime counts by district"""
    return df['PdDistrict'].value_counts()


def get_day_counts(df):
    """get crime counts by day of week"""
    day_counts = df['DayOfWeek'].value_counts()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return day_counts.reindex([d for d in days_order if d in day_counts.index])


def get_resolution_counts(df, n=10):
    """get top n resolution types"""
    return df['Resolution'].value_counts().head(n)


def calculate_cluster_stats(df_sample, labels):
    """calculate statistics for each cluster"""
    df_filtered = df_sample[labels != -1].copy()
    cluster_labels = labels[labels != -1]
    df_filtered['Cluster'] = cluster_labels
    
    cluster_stats = []
    for cluster_id in sorted(df_filtered['Cluster'].unique()):
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        cluster_stats.append({
            'Cluster ID': cluster_id,
            'Number of Points': len(cluster_data),
            'Center Latitude': cluster_data['Y'].mean(),
            'Center Longitude': cluster_data['X'].mean(),
            'Top Crime Type': cluster_data['Category'].mode()[0] if len(cluster_data) > 0 else 'N/A'
        })
    
    return pd.DataFrame(cluster_stats)


def get_cluster_centers(df_sample, labels):
    """calculate center points for each cluster"""
    df_filtered = df_sample[labels != -1].copy()
    cluster_labels = labels[labels != -1]
    df_filtered['Cluster'] = cluster_labels
    
    mean_location_clusters = []
    for group in sorted(df_filtered['Cluster'].unique()):
        cluster_data = df_filtered[df_filtered['Cluster'] == group]
        mean_location_clusters.append([
            cluster_data['X'].mean(),
            cluster_data['Y'].mean()
        ])
    
    return mean_location_clusters, df_filtered

