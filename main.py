import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
import requests
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="DBSCAN Crime Spots Analysis",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        padding: 1rem 0;
    }
    .section-header {
        font-size: 2rem;
        color: #0068C9;
        padding: 1rem 0;
        border-bottom: 2px solid #0068C9;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load the San Francisco crime dataset"""
    url = 'https://ibm.box.com/shared/static/nmcltjmocdi8sd5tk93uembzdec8zyaq.csv'
    df = pd.read_csv(url)
    return df


@st.cache_data
def load_geojson():
    """Load the San Francisco GeoJSON data"""
    geojson_url = 'https://cocl.us/sanfran_geojson'
    response = requests.get(geojson_url)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write(response.text)
        temp_path = f.name
    
    return temp_path, response.text


@st.cache_data
def prepare_district_data(df):
    """Prepare data for district-level analysis"""
    df_san = df[["PdDistrict", "Category"]].groupby("PdDistrict").count()
    df_san = df_san.reset_index()
    df_san.rename(columns={'PdDistrict': 'Neighborhood', 'Category': 'Count'}, inplace=True)
    return df_san


@st.cache_data
def run_dbscan(df, eps, min_samples):
    """Run DBSCAN algorithm on the dataset"""
    df_SF = df[['X', 'Y']].copy()
    
    # Normalization
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df_SF)
    
    # Apply DBSCAN
    crime_points = DBSCAN(eps=eps, min_samples=min_samples).fit(df_scaled)
    labels = crime_points.labels_
    
    # Calculate statistics
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    return labels, n_clusters, n_noise, df_SF


def main():
    # Header
    st.markdown('<h1 class="main-header">🚨 DBSCAN Algorithm for Crime Spot Detection</h1>', 
                unsafe_allow_html=True)
    st.markdown("### Analyzing San Francisco Crime Data with Density-Based Clustering")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Home", "📚 DBSCAN Theory", "📊 Dataset Overview", 
         "📈 Data Visualization", "🎯 DBSCAN Clustering", 
         "🗺️ Interactive Maps", "🔥 Heat Maps", "📑 Summary"]
    )
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    # ==================== HOME PAGE ====================
    if page == "🏠 Home":
        st.markdown('<h2 class="section-header">Welcome to Crime Spot Detection System</h2>', 
                    unsafe_allow_html=True)
        
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
    
    # ==================== DBSCAN THEORY PAGE ====================
    elif page == "📚 DBSCAN Theory":
        st.markdown('<h2 class="section-header">Understanding DBSCAN Algorithm</h2>', 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Overview", "How It Works", "Advantages & Disadvantages"])
        
        with tab1:
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
        
        with tab2:
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
        
        with tab3:
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
    
    # ==================== DATASET OVERVIEW PAGE ====================
    elif page == "📊 Dataset Overview":
        st.markdown('<h2 class="section-header">Dataset Overview</h2>', 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Basic Info", "Sample Data", "Statistics"])
        
        with tab1:
            st.markdown("### Dataset Information")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Records", f"{len(df):,}")
            col2.metric("Features", len(df.columns))
            col3.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            col4.metric("Missing Values", df.isnull().sum().sum())
            
            st.markdown("### Column Descriptions")
            
            feature_info = {
                "IncidntNum": "Unique incident number identifier",
                "Category": "Category of crime or incident",
                "Descript": "Detailed description of the crime",
                "DayOfWeek": "Day of week when incident occurred",
                "Date": "Date of the incident",
                "Time": "Time of day when incident occurred",
                "PdDistrict": "Police department district",
                "Resolution": "How the crime was resolved",
                "Address": "Closest address to incident location",
                "X": "Longitude coordinate",
                "Y": "Latitude coordinate",
                "Location": "Tuple of latitude and longitude",
                "PdId": "Police department ID"
            }
            
            info_df = pd.DataFrame([
                {"Column": col, "Type": str(df[col].dtype), "Description": desc}
                for col, desc in feature_info.items()
            ])
            
            st.dataframe(info_df, use_container_width=True)
        
        with tab2:
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
            if selected_district:
                filtered_df = filtered_df[filtered_df['PdDistrict'].isin(selected_district)]
            if selected_category:
                filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]
            
            st.write(f"**Filtered Results: {len(filtered_df):,} records**")
            st.dataframe(filtered_df.head(20), use_container_width=True)
        
        with tab3:
            st.markdown("### Statistical Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Top 10 Crime Categories")
                category_counts = df['Category'].value_counts().head(10)
                fig, ax = plt.subplots(figsize=(10, 6))
                category_counts.plot(kind='barh', ax=ax, color='steelblue')
                ax.set_xlabel('Number of Incidents')
                ax.set_title('Top 10 Crime Categories')
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.markdown("#### Incidents by Police District")
                district_counts = df['PdDistrict'].value_counts()
                fig, ax = plt.subplots(figsize=(10, 6))
                district_counts.plot(kind='barh', ax=ax, color='coral')
                ax.set_xlabel('Number of Incidents')
                ax.set_title('Incidents by Police District')
                plt.tight_layout()
                st.pyplot(fig)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Incidents by Day of Week")
                day_counts = df['DayOfWeek'].value_counts()
                days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_counts = day_counts.reindex([d for d in days_order if d in day_counts.index])
                fig, ax = plt.subplots(figsize=(10, 6))
                day_counts.plot(kind='bar', ax=ax, color='teal')
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Number of Incidents')
                ax.set_title('Crime Distribution by Day')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.markdown("#### Resolution Status")
                resolution_counts = df['Resolution'].value_counts().head(10)
                fig, ax = plt.subplots(figsize=(10, 6))
                resolution_counts.plot(kind='bar', ax=ax, color='purple')
                ax.set_xlabel('Resolution Type')
                ax.set_ylabel('Count')
                ax.set_title('Top 10 Resolution Types')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
    
    # ==================== DATA VISUALIZATION PAGE ====================
    elif page == "📈 Data Visualization":
        st.markdown('<h2 class="section-header">Data Visualization</h2>', 
                    unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Scatter Plots", "Choropleth Map"])
        
        with tab1:
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
                
                fig, ax = plt.subplots(figsize=(plot_size, plot_size * 0.8))
                plt.title('Location of Crimes Reported in San Francisco', 
                         loc='left', fontsize=16, fontweight='bold')
                sns.scatterplot(x=df_sample.X, y=df_sample.Y, alpha=alpha_value, 
                              color='darkblue', s=10, ax=ax)
                ax.set_xlabel('Longitude', fontsize=12)
                ax.set_ylabel('Latitude', fontsize=12)
                plt.tight_layout()
                st.pyplot(fig)
            
            st.info(f"📊 Displaying {len(df_sample):,} out of {len(df):,} incidents")
        
        with tab2:
            st.markdown("### Crime Rate by District - Choropleth Map")
            st.markdown("""
            This choropleth map shows the crime intensity across different police districts in 
            San Francisco. Darker colors indicate higher crime rates.
            """)
            
            try:
                geojson_path, geojson_data = load_geojson()
                df_san = prepare_district_data(df)
                
                latitude = 37.77
                longitude = -122.42
                
                # Create choropleth map
                sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)
                
                folium.Choropleth(
                    geo_data=geojson_data,
                    data=df_san,
                    columns=['Neighborhood', 'Count'],
                    key_on='feature.properties.DISTRICT',
                    fill_color='YlOrRd',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='Crime Rate in San Francisco'
                ).add_to(sanfran_map)
                
                st_folium(sanfran_map, width=1200, height=600)
                
                st.markdown("#### District Statistics")
                df_san_sorted = df_san.sort_values('Count', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top 5 Districts by Crime Count**")
                    st.dataframe(df_san_sorted.head(), use_container_width=True)
                
                with col2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    df_san_sorted.plot(x='Neighborhood', y='Count', kind='bar', 
                                      ax=ax, color='orangered', legend=False)
                    ax.set_title('Crime Count by District')
                    ax.set_xlabel('District')
                    ax.set_ylabel('Number of Incidents')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error loading choropleth map: {str(e)}")
                st.info("Showing district data in table format instead:")
                df_san = prepare_district_data(df)
                st.dataframe(df_san.sort_values('Count', ascending=False), 
                           use_container_width=True)
    
    # ==================== DBSCAN CLUSTERING PAGE ====================
    elif page == "🎯 DBSCAN Clustering":
        st.markdown('<h2 class="section-header">DBSCAN Clustering Analysis</h2>', 
                    unsafe_allow_html=True)
        
        st.markdown("""
        Adjust the DBSCAN parameters below to see how they affect the clustering results.
        The algorithm will identify crime hotspots and classify outliers.
        """)
        
        # Parameter controls
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
        
        # Run DBSCAN
        df_sample = df.sample(n=min(sample_size, len(df)), random_state=42).copy()
        
        with st.spinner("Running DBSCAN algorithm..."):
            labels, n_clusters, n_noise, df_SF = run_dbscan(df_sample, eps, min_samples)
        
        df_sample['Cluster'] = labels
        
        # Display results
        st.markdown("### Clustering Results")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Clusters Found", n_clusters)
        col2.metric("Noise Points", f"{n_noise:,}")
        col3.metric("Clustered Points", f"{len(df_sample) - n_noise:,}")
        col4.metric("Noise Percentage", f"{(n_noise/len(df_sample)*100):.1f}%")
        
        # Tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["With Noise", "Without Noise", "Cluster Details"])
        
        with tab1:
            st.markdown("#### Crime Spots with Noise Points (Label = -1)")
            
            fig, ax = plt.subplots(figsize=(12, 10))
            scatter = sns.scatterplot(
                x=df_sample.X, 
                y=df_sample.Y, 
                hue=labels,
                palette='tab20',
                alpha=0.4,
                s=15,
                ax=ax,
                legend='auto'
            )
            plt.title('Crime Spots in San Francisco - DBSCAN with Noise', 
                     fontsize=16, fontweight='bold', loc='left')
            plt.xlabel('Longitude', fontsize=12)
            plt.ylabel('Latitude', fontsize=12)
            
            # Move legend outside plot
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
                      title='Cluster', ncol=1)
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            st.markdown("#### Crime Spots without Noise Points")
            
            # Filter out noise
            df_filtered = df_sample[df_sample['Cluster'] != -1].copy()
            labels_filtered = labels[labels != -1]
            
            if len(df_filtered) > 0:
                # Calculate cluster centers
                mean_location_clusters = []
                for group in np.unique(labels_filtered):
                    cluster_data = df_filtered[df_filtered['Cluster'] == group]
                    mean_location_clusters.append([
                        cluster_data['X'].mean(),
                        cluster_data['Y'].mean()
                    ])
                
                fig, ax = plt.subplots(figsize=(12, 10))
                sns.scatterplot(
                    x=df_filtered.X,
                    y=df_filtered.Y,
                    hue=df_filtered['Cluster'],
                    palette='tab20',
                    alpha=0.4,
                    s=15,
                    ax=ax,
                    legend=None
                )
                
                # Add cluster labels
                for index, location in enumerate(mean_location_clusters):
                    plt.text(location[0], location[1], str(index), 
                           fontsize=16, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='white', 
                                   edgecolor='black', alpha=0.7))
                
                plt.title('Crime Spots in San Francisco - DBSCAN without Noise', 
                         fontsize=16, fontweight='bold', loc='left')
                plt.xlabel('Longitude', fontsize=12)
                plt.ylabel('Latitude', fontsize=12)
                plt.tight_layout()
                st.pyplot(fig)
                
                st.success(f"✅ Successfully identified {n_clusters} crime hotspot clusters!")
            else:
                st.warning("No clusters found with current parameters. Try adjusting eps or min_samples.")
        
        with tab3:
            st.markdown("#### Detailed Cluster Information")
            
            if n_clusters > 0:
                df_filtered = df_sample[df_sample['Cluster'] != -1].copy()
                
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
                
                cluster_df = pd.DataFrame(cluster_stats)
                st.dataframe(cluster_df, use_container_width=True)
                
                # Cluster size distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    cluster_sizes = df_filtered['Cluster'].value_counts().sort_index()
                    cluster_sizes.plot(kind='bar', ax=ax, color='steelblue')
                    ax.set_title('Points per Cluster')
                    ax.set_xlabel('Cluster ID')
                    ax.set_ylabel('Number of Points')
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    noise_data = pd.DataFrame({
                        'Type': ['Clustered Points', 'Noise Points'],
                        'Count': [len(df_sample) - n_noise, n_noise]
                    })
                    ax.pie(noise_data['Count'], labels=noise_data['Type'], 
                          autopct='%1.1f%%', startangle=90,
                          colors=['lightgreen', 'lightcoral'])
                    ax.set_title('Clustered vs Noise Points')
                    st.pyplot(fig)
            else:
                st.warning("No clusters found. Try different parameters.")
    
    # ==================== INTERACTIVE MAPS PAGE ====================
    elif page == "🗺️ Interactive Maps":
        st.markdown('<h2 class="section-header">Interactive Map Visualizations</h2>', 
                    unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Cluster Centers", 
            "Crime Markers", 
            "Marker Clusters",
            "Combined View"
        ])
        
        # Run DBSCAN for maps
        eps = 0.020
        min_samples = 500
        sample_size = min(50000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42).copy()
        
        with st.spinner("Preparing map data..."):
            labels, n_clusters, n_noise, df_SF = run_dbscan(df_sample, eps, min_samples)
            df_sample['Cluster'] = labels
        
        # Calculate cluster centers
        df_filtered = df_sample[df_sample['Cluster'] != -1].copy()
        mean_location_clusters = []
        
        if len(df_filtered) > 0:
            for group in np.unique(df_filtered['Cluster']):
                cluster_data = df_filtered[df_filtered['Cluster'] == group]
                mean_location_clusters.append([
                    cluster_data['X'].mean(),
                    cluster_data['Y'].mean()
                ])
        
        latitude = 37.77
        longitude = -122.42
        
        with tab1:
            st.markdown("### DBSCAN Cluster Centers")
            st.markdown("""
            This map shows the center points of identified crime clusters. Each marker represents
            a high-density crime area.
            """)
            
            SF_map = folium.Map(location=[latitude, longitude], zoom_start=13)
            
            # Add cluster centers with numbered markers
            for index, location in enumerate(mean_location_clusters):
                folium.Marker(
                    location=[location[1], location[0]],
                    popup=f"Cluster {index}<br>{df_filtered[df_filtered['Cluster']==index].shape[0]} crimes",
                    tooltip=f"Cluster {index}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(SF_map)
            
            st_folium(SF_map, width=1200, height=600)
            
            st.info(f"🎯 Showing {len(mean_location_clusters)} cluster centers")
        
        with tab2:
            st.markdown("### Individual Crime Markers")
            st.markdown("""
            Shows individual crime incidents as circle markers. Click on markers to see crime category.
            Limited to first 1000 incidents for performance.
            """)
            
            limit = st.slider("Number of incidents to display", 100, 2000, 1000, 100)
            
            SF_map2 = folium.Map(location=[latitude, longitude], zoom_start=13)
            
            df_incidents = df_sample.iloc[:limit, :]
            
            # Add circle markers
            for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
                folium.CircleMarker(
                    [lat, lng],
                    radius=3,
                    color='blue',
                    fill=True,
                    popup=label,
                    fill_color='cyan',
                    fill_opacity=0.5
                ).add_to(SF_map2)
            
            st_folium(SF_map2, width=1200, height=600)
            
            st.info(f"📍 Displaying {min(limit, len(df_incidents)):,} crime markers")
        
        with tab3:
            st.markdown("### Marker Clustering")
            st.markdown("""
            Incidents are grouped into clusters for better visualization. Zoom in to see individual 
            markers. Numbers indicate how many incidents are in each cluster.
            """)
            
            limit = st.slider("Number of incidents for clustering", 500, 5000, 2000, 500)
            
            SF_map3 = folium.Map(location=[latitude, longitude], zoom_start=12)
            
            # Create marker cluster
            marker_cluster = plugins.MarkerCluster().add_to(SF_map3)
            
            df_incidents = df_sample.iloc[:limit, :]
            
            # Add markers to cluster
            for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
                folium.Marker(
                    location=[lat, lng],
                    popup=f"<b>{label}</b>",
                    tooltip=label
                ).add_to(marker_cluster)
            
            st_folium(SF_map3, width=1200, height=600)
            
            st.info(f"🗂️ Clustering {min(limit, len(df_incidents)):,} incidents")
        
        with tab4:
            st.markdown("### Combined View: Clusters + Crime Points")
            st.markdown("""
            This map combines cluster centers (red markers) with individual crime incidents 
            (blue circles) for a comprehensive view.
            """)
            
            SF_map4 = folium.Map(location=[latitude, longitude], zoom_start=13)
            
            # Add cluster centers
            for index, location in enumerate(mean_location_clusters):
                folium.Marker(
                    location=[location[1], location[0]],
                    popup=f"<b>Cluster {index}</b><br>{df_filtered[df_filtered['Cluster']==index].shape[0]} crimes",
                    tooltip=f"Cluster {index}",
                    icon=folium.Icon(color='red', icon='star', prefix='fa')
                ).add_to(SF_map4)
            
            # Add sample of crime points
            df_incidents = df_sample.iloc[:500, :]
            
            for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
                folium.CircleMarker(
                    [lat, lng],
                    radius=2,
                    color='blue',
                    fill=True,
                    popup=label,
                    fill_color='lightblue',
                    fill_opacity=0.4
                ).add_to(SF_map4)
            
            st_folium(SF_map4, width=1200, height=600)
            
            st.info(f"🗺️ Showing {len(mean_location_clusters)} clusters and 500 crime points")
    
    # ==================== HEAT MAPS PAGE ====================
    elif page == "🔥 Heat Maps":
        st.markdown('<h2 class="section-header">Heat Map Analysis</h2>', 
                    unsafe_allow_html=True)
        
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
            latitude = 37.77
            longitude = -122.42
            
            # Create heat map
            SF_heat_map = folium.Map(
                location=[latitude, longitude], 
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Sample data for heat map
            df_heat = df.sample(n=min(sample_size, len(df)), random_state=42)
            heat_data = [[row['Y'], row['X']] for idx, row in df_heat.iterrows()]
            
            # Add heat layer
            HeatMap(
                heat_data,
                radius=radius,
                blur=blur,
                max_zoom=13,
                min_opacity=0.3,
                max_val=max_intensity
            ).add_to(SF_heat_map)
            
            st_folium(SF_heat_map, width=900, height=600)
        
        st.info(f"🔥 Heat map generated from {len(df_heat):,} incidents")
        
        # Additional analysis
        st.markdown("### Heat Map Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Incidents Analyzed", f"{len(df_heat):,}")
        
        with col2:
            # Find the area with most crimes (approximate)
            lat_bins = pd.cut(df_heat['Y'], bins=10)
            lon_bins = pd.cut(df_heat['X'], bins=10)
            grid_counts = df_heat.groupby([lat_bins, lon_bins]).size()
            max_grid = grid_counts.max()
            st.metric("Max Density Grid", f"{max_grid} crimes")
        
        with col3:
            avg_crimes = len(df_heat) / 100  # Approximate grid cells
            st.metric("Avg per Area", f"{avg_crimes:.0f}")
        
        st.markdown("""
        #### Understanding Heat Maps
        
        - **Red/Bright areas**: High concentration of crimes (hotspots)
        - **Yellow/Orange areas**: Moderate crime activity
        - **Blue/Dark areas**: Low crime activity
        - **No color**: Minimal to no reported incidents
        
        Use the sliders to adjust visualization parameters and explore different perspectives of the data.
        """)
    
    # ==================== SUMMARY PAGE ====================
    elif page == "📑 Summary":
        st.markdown('<h2 class="section-header">Summary & Insights</h2>', 
                    unsafe_allow_html=True)
        
        # Run final analysis
        eps = 0.020
        min_samples = 500
        sample_size = min(50000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42).copy()
        
        labels, n_clusters, n_noise, df_SF = run_dbscan(df_sample, eps, min_samples)
        df_sample['Cluster'] = labels
        
        # Key Metrics
        st.markdown("### Key Findings")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Crime Incidents", f"{len(df):,}")
        col2.metric("Crime Hotspots Identified", n_clusters)
        col3.metric("Police Districts", df['PdDistrict'].nunique())
        col4.metric("Crime Categories", df['Category'].nunique())
        
        st.markdown("---")
        
        # Insights
        col1, col2 = st.columns(2)
        
        with col1:
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
        
        with col2:
            st.markdown("### 🎯 DBSCAN Results")
            
            clustered_pct = ((len(df_sample) - n_noise) / len(df_sample)) * 100
            
            st.markdown(f"""
            - **Clusters Identified**: {n_clusters} distinct crime hotspots
            - **Clustered Points**: {len(df_sample) - n_noise:,} ({clustered_pct:.1f}%)
            - **Outliers Detected**: {n_noise:,} ({(n_noise/len(df_sample)*100):.1f}%)
            - **Parameters Used**: eps=0.020, min_samples=500
            - **Algorithm**: Successfully identified high-density crime areas
            """)
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            #### For Law Enforcement
            
            1. **Focus Resources**: Prioritize the identified hotspot clusters
            2. **Patrol Optimization**: Increase presence in high-density areas
            3. **Prevention Programs**: Target top crime categories
            4. **Time-based Strategy**: Deploy more officers on peak days
            5. **District Coordination**: Share insights across districts
            """)
        
        with col2:
            st.info("""
            #### For Further Analysis
            
            1. **Temporal Analysis**: Study crime patterns by time of day
            2. **Seasonal Trends**: Analyze crime variations across seasons
            3. **Crime Type Clustering**: Separate analysis for different crime types
            4. **Predictive Modeling**: Build models to forecast crime hotspots
            5. **Socioeconomic Factors**: Correlate with demographic data
            """)
        
        st.markdown("---")
        
        # Technical Summary
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
        
        st.markdown("---")
        
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>DBSCAN Crime Spots Analysis | San Francisco Police Department Data 2016</p>
        <p>Built with Streamlit, Scikit-learn, Folium, and Pandas</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
