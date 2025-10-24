"""
dbscan theory page - educational content about the algorithm
"""

import streamlit as st
from src.utils.ui_helpers import render_section_header


def render_theory_page():
    """render the dbscan theory and explanation page"""
    render_section_header("Understanding DBSCAN Algorithm")
    
    tab1, tab2, tab3 = st.tabs(["Overview", "How It Works", "Advantages & Disadvantages"])
    
    with tab1:
        _render_overview_tab()
    
    with tab2:
        _render_how_it_works_tab()
    
    with tab3:
        _render_pros_cons_tab()


def _render_overview_tab():
    """render the overview tab"""
    st.markdown("""
    ### What is DBSCAN?
    
    **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) is a density-based 
    clustering algorithm used to separate high-density regions from low-density regions.
    
    Unlike K-means, DBSCAN:
    - **Does not require** specifying the number of clusters beforehand
    - **Can find** arbitrarily shaped clusters (not just spherical)
    - **Can identify** outliers and noise in the data
    - **Works well** with spatial/geographic data
    """)
    
    st.image("https://miro.medium.com/max/1400/1*tc8UF-h0nQqUfLC8-0uInQ.gif", 
             caption="DBSCAN Clustering Visualization")


def _render_how_it_works_tab():
    """render the how it works tab"""
    st.markdown("""
    ### Key Concepts
    
    #### 1. Hyperparameters
    
    DBSCAN requires two main hyperparameters:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **ε (eps) - Radius:**
        - Maximum distance between two points to be considered neighbors
        - Defines the neighborhood size
        - Smaller values → more clusters
        - Larger values → fewer clusters
        """)
    
    with col2:
        st.markdown("""
        **MinPts (min_samples) - Minimum Points:**
        - Minimum number of points required to form a dense region
        - A point needs at least MinPts neighbors (including itself) to be a core point
        - Higher values → stricter cluster formation
        - Lower values → more flexible clustering
        """)
    
    st.markdown("""
    #### 2. Point Classification
    
    DBSCAN classifies each point into one of three categories:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔵 Core Point**
        
        A point with at least MinPts points within its ε-neighborhood (including itself)
        """)
    
    with col2:
        st.warning("""
        **🟡 Border Point**
        
        A point within ε distance of a core point, but has fewer than MinPts neighbors
        """)
    
    with col3:
        st.error("""
        **🔴 Outlier/Noise**
        
        A point that is neither a core point nor a border point
        """)
    
    st.markdown("""
    #### 3. Algorithm Steps
    
    1. **Pick a point** that hasn't been visited
    2. **Find all points** within ε distance
    3. **If points ≥ MinPts**: Start a new cluster
        - Add all neighbor points to cluster
        - Recursively expand cluster by checking neighbors
    4. **If points < MinPts**: Mark as noise (may be changed later)
    5. **Repeat** until all points are visited
    """)


def _render_pros_cons_tab():
    """render the advantages and disadvantages tab"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✅ Advantages
        
        - **No need to specify** number of clusters
        - **Finds arbitrary shaped** clusters
        - **Identifies outliers** and noise
        - **Robust to outliers** in the data
        - **Works well** with spatial data
        - **Deterministic results** (mostly)
        - **Single scan** of database
        """)
    
    with col2:
        st.warning("""
        ### ⚠️ Disadvantages
        
        - **Parameter selection** can be challenging
        - **Struggles with** varying density clusters
        - **Not suitable** for high-dimensional data
        - **Border points** may change clusters
        - **Performance** depends on distance metric
        - **Memory intensive** for large datasets
        """)
    
    st.info("""
    ### 💡 Best Use Cases
    
    DBSCAN works best for:
    - **Spatial/Geographic data** (like our crime spots!)
    - **Anomaly detection**
    - **Data with noise** or outliers
    - **Non-globular cluster shapes**
    - **Unknown number of clusters**
    """)

