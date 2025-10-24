"""
app configuration and constants
"""

# dataset urls
DATA_URL = 'https://ibm.box.com/shared/static/nmcltjmocdi8sd5tk93uembzdec8zyaq.csv'
GEOJSON_URL = 'https://cocl.us/sanfran_geojson'

# map defaults
SF_LATITUDE = 37.77
SF_LONGITUDE = -122.42
DEFAULT_ZOOM = 12

# dbscan defaults
DEFAULT_EPS = 0.020
DEFAULT_MIN_SAMPLES = 500
DEFAULT_SAMPLE_SIZE = 50000

# plot settings
PLOT_ALPHA = 0.35
PLOT_SIZE = 12
DEFAULT_MARKER_SIZE = 10

# color schemes
CLUSTER_PALETTE = 'tab20'
CHOROPLETH_COLORS = 'YlOrRd'

# page config
PAGE_TITLE = "DBSCAN Crime Spots Analysis"
PAGE_ICON = "🚨"
LAYOUT = "wide"

# styling
CUSTOM_CSS = """
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
"""

