"""
summary page - key findings and insights
"""

import streamlit as st

from src.utils.ui_helpers import render_section_header
from src.models.dbscan_model import run_dbscan
from src.config.settings import DEFAULT_EPS, DEFAULT_MIN_SAMPLES


def render_summary_page(df):
    """render the summary and insights page"""
    render_section_header("Summary & Insights")
    
    # run final analysis
    sample_size = min(50000, len(df))
    df_sample = df.sample(n=sample_size, random_state=42).copy()
    
    labels, n_clusters, n_noise, df_SF = run_dbscan(
        df_sample, DEFAULT_EPS, DEFAULT_MIN_SAMPLES
    )
    df_sample['Cluster'] = labels
    
    # key metrics
    st.markdown("### Key Findings")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Crime Incidents", f"{len(df):,}")
    col2.metric("Crime Hotspots Identified", n_clusters)
    col3.metric("Police Districts", df['PdDistrict'].nunique())
    col4.metric("Crime Categories", df['Category'].nunique())
    
    st.markdown("---")
    
    # insights
    col1, col2 = st.columns(2)
    
    with col1:
        _render_dataset_insights(df)
    
    with col2:
        _render_dbscan_insights(df_sample, n_clusters, n_noise)
    
    st.markdown("---")
    
    # recommendations
    st.markdown("### 💡 Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_law_enforcement_recommendations()
    
    with col2:
        _render_further_analysis_recommendations()
    
    st.markdown("---")
    
    # technical summary
    _render_technical_summary()
    
    st.markdown("---")
    
    _render_application_features()


def _render_dataset_insights(df):
    """render dataset insights section"""
    st.markdown("### 📊 Dataset Insights")
    
    top_category = df['Category'].value_counts().index[0]
    top_category_count = df['Category'].value_counts().values[0]
    top_district = df['PdDistrict'].value_counts().index[0]
    top_day = df['DayOfWeek'].value_counts().index[0]
    
    st.markdown(f"""
    - **Most Common Crime**: {top_category} ({top_category_count:,} incidents)
    - **Busiest District**: {top_district}
    - **Peak Day**: {top_day}
    - **Geographic Spread**: Across {df['PdDistrict'].nunique()} districts
    - **Data Completeness**: {(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))):.1%}
    """)


def _render_dbscan_insights(df_sample, n_clusters, n_noise):
    """render dbscan results section"""
    st.markdown("### 🎯 DBSCAN Results")
    
    clustered_pct = ((len(df_sample) - n_noise) / len(df_sample)) * 100
    
    st.markdown(f"""
    - **Clusters Identified**: {n_clusters} distinct crime hotspots
    - **Clustered Points**: {len(df_sample) - n_noise:,} ({clustered_pct:.1f}%)
    - **Outliers Detected**: {n_noise:,} ({(n_noise/len(df_sample)*100):.1f}%)
    - **Parameters Used**: eps=0.020, min_samples=500
    - **Algorithm**: Successfully identified high-density crime areas
    """)


def _render_law_enforcement_recommendations():
    """render law enforcement recommendations"""
    st.success("""
    #### For Law Enforcement
    
    1. **Focus Resources**: Prioritize the identified hotspot clusters
    2. **Patrol Optimization**: Increase presence in high-density areas
    3. **Prevention Programs**: Target top crime categories
    4. **Time-based Strategy**: Deploy more officers on peak days
    5. **District Coordination**: Share insights across districts
    """)


def _render_further_analysis_recommendations():
    """render further analysis recommendations"""
    st.info("""
    #### For Further Analysis
    
    1. **Temporal Analysis**: Study crime patterns by time of day
    2. **Seasonal Trends**: Analyze crime variations across seasons
    3. **Crime Type Clustering**: Separate analysis for different crime types
    4. **Predictive Modeling**: Build models to forecast crime hotspots
    5. **Socioeconomic Factors**: Correlate with demographic data
    """)


def _render_technical_summary():
    """render technical summary section"""
    st.markdown("### 🔧 Technical Summary")
    
    st.markdown("""
    #### DBSCAN Algorithm Performance
    
    The DBSCAN algorithm successfully identified crime hotspots in San Francisco by:
    
    1. **Normalizing** geographic coordinates using MinMaxScaler
    2. **Clustering** based on spatial density with configurable parameters
    3. **Identifying** outliers and noise points in the data
    4. **Detecting** arbitrary-shaped clusters (not limited to spherical shapes)
    
    #### Advantages of This Approach
    
    - ✅ **No predetermined cluster count** required
    - ✅ **Handles noise** and outliers effectively
    - ✅ **Finds arbitrary shapes** in geographic data
    - ✅ **Scalable** to large datasets with sampling
    - ✅ **Interpretable results** for actionable insights
    
    #### Visualization Tools Used
    
    - **Matplotlib & Seaborn**: Statistical plots and scatter visualizations
    - **Folium**: Interactive geographic maps
    - **Streamlit**: Interactive web application
    - **Choropleth Maps**: District-level crime intensity
    - **Heat Maps**: Density-based crime visualization
    """)


def _render_application_features():
    """render application features summary"""
    st.success("""
    ### ✨ Application Features
    
    This application successfully demonstrates:
    
    - 📊 **Comprehensive data exploration** with interactive filters
    - 📚 **Educational content** about DBSCAN algorithm
    - 🎯 **Interactive parameter tuning** for clustering
    - 🗺️ **Multiple map visualizations** (choropleth, markers, clusters, heatmaps)
    - 📈 **Statistical analysis** and insights
    - 💡 **Actionable recommendations** for stakeholders
    
    Use the sidebar to navigate through different sections and explore the analysis!
    """)

