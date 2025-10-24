"""
dataset overview page - explore and understand the data
"""

import streamlit as st
import pandas as pd

from src.utils.ui_helpers import render_section_header, display_feature_info
from src.data.processor import (
    filter_by_district, filter_by_category,
    get_top_categories, get_district_counts, 
    get_day_counts, get_resolution_counts
)
from src.visualization.plots import (
    plot_top_categories, plot_district_counts,
    plot_day_distribution, plot_resolution_status
)


def render_dataset_overview_page(df):
    """render the dataset overview page"""
    render_section_header("Dataset Overview")
    
    tab1, tab2, tab3 = st.tabs(["Basic Info", "Sample Data", "Statistics"])
    
    with tab1:
        _render_basic_info_tab(df)
    
    with tab2:
        _render_sample_data_tab(df)
    
    with tab3:
        _render_statistics_tab(df)


def _render_basic_info_tab(df):
    """render basic info about the dataset"""
    st.markdown("### Dataset Information")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Features", len(df.columns))
    col3.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    col4.metric("Missing Values", df.isnull().sum().sum())
    
    st.markdown("### Column Descriptions")
    
    feature_info = display_feature_info()
    info_df = pd.DataFrame([
        {"Column": col, "Type": str(df[col].dtype), "Description": desc}
        for col, desc in feature_info.items()
    ])
    
    st.dataframe(info_df, use_container_width=True)


def _render_sample_data_tab(df):
    """render sample data browser"""
    st.markdown("### Sample Data")
    
    num_rows = st.slider("Number of rows to display", 5, 100, 10)
    display_option = st.radio("Display", ["First rows", "Random sample"], horizontal=True)
    
    if display_option == "First rows":
        st.dataframe(df.head(num_rows), use_container_width=True)
    else:
        st.dataframe(df.sample(num_rows), use_container_width=True)
    
    st.markdown("### Filter Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_district = st.multiselect(
            "Select Police District(s)",
            options=sorted(df['PdDistrict'].dropna().unique())
        )
    
    with col2:
        selected_category = st.multiselect(
            "Select Crime Category",
            options=sorted(df['Category'].unique())
        )
    
    filtered_df = df.copy()
    filtered_df = filter_by_district(filtered_df, selected_district)
    filtered_df = filter_by_category(filtered_df, selected_category)
    
    st.write(f"**Filtered Results: {len(filtered_df):,} records**")
    st.dataframe(filtered_df.head(20), use_container_width=True)


def _render_statistics_tab(df):
    """render statistical visualizations"""
    st.markdown("### Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Crime Categories")
        category_counts = get_top_categories(df, 10)
        fig = plot_top_categories(category_counts)
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### Incidents by Police District")
        district_counts = get_district_counts(df)
        fig = plot_district_counts(district_counts)
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Incidents by Day of Week")
        day_counts = get_day_counts(df)
        fig = plot_day_distribution(day_counts)
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### Resolution Status")
        resolution_counts = get_resolution_counts(df, 10)
        fig = plot_resolution_status(resolution_counts)
        st.pyplot(fig)

