# 🚨 DBSCAN Crime Spots Analysis

An interactive Streamlit application for analyzing San Francisco crime data using the DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm.

## Try it now:
[Launch Streamlit App](https://dbscan-crime-spots-utsavj.streamlit.app/)

Deployed it using the community tier of Streamlit. Not sure about the reliability and uptime of the app. If something goes wrong, here's the demo video for what the app looks like.👇

## DEMO VIDEO👇
[streamlit-main-2025-10-24-11-10-16.webm](https://github.com/user-attachments/assets/fcd50f5d-fde8-4e9c-a6bb-d1f8458c5bca)

## 📋 Overview

This application demonstrates the power of DBSCAN clustering for identifying crime hotspots in San Francisco. It provides:

- **Interactive Data Exploration**: Browse and filter 150,500+ crime incidents
- **Educational Content**: Learn how DBSCAN algorithm works
- **Real-time Clustering**: Adjust parameters and see results instantly
- **Advanced Visualizations**: Multiple map types including choropleth, markers, clusters, and heatmaps
- **Statistical Analysis**: Detailed insights into crime patterns

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- uv (Python package manager) - recommended

### Installation

1. **Clone or navigate to the repository:**
   ```bash
   cd dbscan_crime_spots
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn scikit-learn folium streamlit-folium requests
   ```

### Running the Application

**Using uv:**
```bash
uv run streamlit run main.py
```

**Using standard Python:**
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Features

### 1. Home Page
- Quick statistics overview
- Introduction to the application
- Dataset information

### 2. DBSCAN Theory
- **Overview**: Introduction to DBSCAN algorithm
- **How It Works**: Detailed explanation with key concepts
- **Advantages & Disadvantages**: Comprehensive analysis

### 3. Dataset Overview
- **Basic Info**: Dataset statistics and column descriptions
- **Sample Data**: Interactive data browsing with filters
- **Statistics**: Visual analysis of crime patterns

### 4. Data Visualization
- **Scatter Plots**: Geographic distribution of crimes
- **Choropleth Maps**: Crime intensity by police district

### 5. DBSCAN Clustering
- **Interactive Parameters**: Adjust epsilon and min_samples
- **Multiple Views**: With/without noise visualization
- **Cluster Details**: Statistical breakdown of each cluster

### 6. Interactive Maps
- **Cluster Centers**: Identified crime hotspots
- **Crime Markers**: Individual incident locations
- **Marker Clusters**: Grouped visualization for better performance
- **Combined View**: Comprehensive overview

### 7. Heat Maps
- **Density Visualization**: Intuitive crime concentration display
- **Adjustable Parameters**: Customize radius, blur, and intensity
- **Real-time Updates**: Interactive exploration

### 8. Summary
- **Key Findings**: Statistical insights
- **Recommendations**: Actionable suggestions
- **Technical Summary**: Algorithm performance details

## 📁 Project Structure

```
dbscan_crime_spots/
├── main.py                          # Application entry point
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration and constants
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py                # Data loading utilities
│   │   └── processor.py             # Data processing and transformation
│   ├── models/
│   │   ├── __init__.py
│   │   └── dbscan_model.py          # DBSCAN clustering implementation
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py                  # Home page
│   │   ├── theory.py                # DBSCAN theory page
│   │   ├── dataset_overview.py     # Dataset exploration
│   │   ├── data_visualization.py   # Scatter plots and maps
│   │   ├── dbscan_clustering.py    # Interactive clustering
│   │   ├── interactive_maps.py     # Map visualizations
│   │   ├── heat_maps.py            # Heat map analysis
│   │   └── summary.py              # Summary and insights
│   ├── utils/
│   │   ├── __init__.py
│   │   └── ui_helpers.py           # UI helper functions
│   └── visualization/
│       ├── __init__.py
│       ├── plots.py                # Matplotlib/Seaborn plots
│       └── maps.py                 # Folium map creation
├── pyproject.toml                  # Project dependencies
└── README.md                       # This file
```

## 🛠️ Technology Stack

- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: DBSCAN implementation
- **Matplotlib & Seaborn**: Statistical visualizations
- **Folium**: Interactive maps
- **Streamlit-Folium**: Folium integration with Streamlit

## 🎨 Code Organization

The codebase follows a modular architecture with clear separation of concerns:

- **config/**: Application settings and constants
- **data/**: Data loading and processing logic
- **models/**: Machine learning models (DBSCAN)
- **pages/**: Individual Streamlit page components
- **utils/**: Utility functions and helpers
- **visualization/**: Plotting and mapping functions

## 📖 Usage Tips

1. **Start with Home**: Get an overview of the application
2. **Learn DBSCAN**: Understand the algorithm before using it
3. **Explore Data**: Browse the dataset to understand its structure
4. **Adjust Parameters**: Experiment with different epsilon and min_samples values
5. **Compare Views**: Use different map types to gain different insights

## 🎯 DBSCAN Parameters

- **Epsilon (ε)**: Controls the neighborhood radius
  - Smaller values → More clusters
  - Larger values → Fewer, larger clusters
  - Recommended range: 0.001 - 0.050

- **Min Samples**: Minimum points to form a cluster
  - Higher values → Stricter clustering
  - Lower values → More flexible clustering
  - Recommended range: 50 - 1000

## 📊 Dataset Information

- **Source**: San Francisco Police Department
- **Year**: 2016
- **Records**: 150,500 crime incidents
- **Features**: 13 columns including location, category, time, and resolution

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements!

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- San Francisco Police Department for the dataset
- IBM for hosting the data
- Scikit-learn team for the DBSCAN implementation

