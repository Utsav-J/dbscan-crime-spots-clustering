"""
helper functions for streamlit ui components
"""

import streamlit as st


def render_header(text, css_class="main-header"):
    """render a styled header"""
    st.markdown(f'<h1 class="{css_class}">{text}</h1>', unsafe_allow_html=True)


def render_section_header(text):
    """render a section header"""
    st.markdown(f'<h2 class="section-header">{text}</h2>', unsafe_allow_html=True)


def render_metrics_row(metrics_dict):
    """render a row of metrics"""
    cols = st.columns(len(metrics_dict))
    for col, (label, value) in zip(cols, metrics_dict.items()):
        col.metric(label, value)


def create_sidebar_navigation():
    """create modern sidebar navigation menu with clickable buttons"""
    
    # initialize session state for current page if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    
    # sidebar header
    st.sidebar.title("🗺️ Navigation")
    st.sidebar.markdown("---")
    
    # define all pages
    pages = [
        "🏠 Home",
        "📚 DBSCAN Theory",
        "📊 Dataset Overview",
        "📈 Data Visualization",
        "🎯 DBSCAN Clustering",
        "🗺️ Interactive Maps",
        "🔥 Heat Maps",
        "📑 Summary"
    ]
    
    # create clickable buttons for each page
    for page in pages:
        # check if this is the current page
        is_current = st.session_state.current_page == page
        
        # create button with appropriate styling
        if st.sidebar.button(
            page,
            key=f"nav_{page}",
            type="primary" if is_current else "secondary",
            use_container_width=True
        ):
            st.session_state.current_page = page
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # add some helpful info at the bottom
    st.sidebar.markdown("""
    <div style='margin-top: 2rem; padding: 1rem; background: rgba(255, 75, 75, 0.1); border-radius: 0.5rem; border-left: 4px solid #FF4B4B;'>
        <p style='margin: 0; font-size: 0.9rem; opacity: 0.8;'>
            <b>💡 Tip:</b> Click any button above to navigate between sections
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.current_page


def display_feature_info():
    """display dataset feature descriptions"""
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
    return feature_info

