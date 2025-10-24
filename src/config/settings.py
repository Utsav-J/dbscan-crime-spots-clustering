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
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Make sidebar content larger and easier to interact with */
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Style the buttons to be modern and bigger */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        border-radius: 0.75rem;
        font-size: 1.1rem;
        font-weight: 500;
        border: 2px solid rgba(128, 128, 128, 0.2);
        transition: all 0.3s ease;
        text-align: left;
        padding-left: 1.25rem;
        background: rgba(128, 128, 128, 0.1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    
    .stButton > button:hover {
        border-color: #FF4B4B;
        background: rgba(255, 75, 75, 0.15);
        box-shadow: 0 4px 8px rgba(255,75,75,0.3);
        transform: translateX(4px);
    }
    
    /* Active button style */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF4B4B 0%, #ff6b6b 100%);
        color: white !important;
        border-color: #FF4B4B;
        box-shadow: 0 4px 12px rgba(255,75,75,0.4);
        font-weight: 600;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #ff3838 0%, #ff5555 100%);
        transform: translateX(4px);
        box-shadow: 0 4px 16px rgba(255,75,75,0.5);
    }
    
    /* Sidebar title styling */
    section[data-testid="stSidebar"] h1 {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #FF4B4B;
    }
    
    /* Sidebar divider */
    section[data-testid="stSidebar"] hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #FF4B4B 50%, transparent 100%);
    }
    </style>
"""

