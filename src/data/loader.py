"""
handles loading crime data from various sources
"""

import streamlit as st
import pandas as pd
import requests
import tempfile

from src.config.settings import DATA_URL, GEOJSON_URL


@st.cache_data
def load_crime_data():
    """load the san francisco crime dataset"""
    df = pd.read_csv(DATA_URL)
    return df


@st.cache_data
def load_geojson():
    """load san francisco geojson for map boundaries"""
    response = requests.get(GEOJSON_URL)
    
    # save to temp file for folium
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write(response.text)
        temp_path = f.name
    
    return temp_path, response.text


def get_sample_data(df, sample_size, random_state=42):
    """get a random sample from the dataset"""
    return df.sample(n=min(sample_size, len(df)), random_state=random_state).copy()

