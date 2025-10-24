"""
folium map creation and visualization functions
"""

import folium
from folium import plugins
from folium.plugins import HeatMap

from src.config.settings import (
    SF_LATITUDE, SF_LONGITUDE, DEFAULT_ZOOM, CHOROPLETH_COLORS
)


def create_base_map(latitude=SF_LATITUDE, longitude=SF_LONGITUDE, zoom=DEFAULT_ZOOM):
    """create a basic folium map centered on san francisco"""
    return folium.Map(location=[latitude, longitude], zoom_start=zoom)


def create_choropleth_map(geojson_data, df_san):
    """create choropleth map showing crime rates by district"""
    sanfran_map = create_base_map()
    
    folium.Choropleth(
        geo_data=geojson_data,
        data=df_san,
        columns=['Neighborhood', 'Count'],
        key_on='feature.properties.DISTRICT',
        fill_color=CHOROPLETH_COLORS,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Crime Rate in San Francisco'
    ).add_to(sanfran_map)
    
    return sanfran_map


def create_cluster_center_map(mean_location_clusters, df_filtered):
    """create map with cluster center markers"""
    sf_map = create_base_map(zoom=13)
    
    for index, location in enumerate(mean_location_clusters):
        cluster_size = df_filtered[df_filtered['Cluster'] == index].shape[0]
        folium.Marker(
            location=[location[1], location[0]],
            popup=f"Cluster {index}<br>{cluster_size} crimes",
            tooltip=f"Cluster {index}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(sf_map)
    
    return sf_map


def create_circle_marker_map(df_incidents, limit=1000):
    """create map with individual crime circle markers"""
    sf_map = create_base_map(zoom=13)
    
    for lat, lng, label in zip(df_incidents.Y[:limit], 
                               df_incidents.X[:limit], 
                               df_incidents.Category[:limit]):
        folium.CircleMarker(
            [lat, lng],
            radius=3,
            color='blue',
            fill=True,
            popup=label,
            fill_color='cyan',
            fill_opacity=0.5
        ).add_to(sf_map)
    
    return sf_map


def create_marker_cluster_map(df_incidents, limit=2000):
    """create map with clustered markers for better performance"""
    sf_map = create_base_map()
    marker_cluster = plugins.MarkerCluster().add_to(sf_map)
    
    for lat, lng, label in zip(df_incidents.Y[:limit], 
                               df_incidents.X[:limit], 
                               df_incidents.Category[:limit]):
        folium.Marker(
            location=[lat, lng],
            popup=f"<b>{label}</b>",
            tooltip=label
        ).add_to(marker_cluster)
    
    return sf_map


def create_combined_map(mean_location_clusters, df_filtered, df_incidents):
    """create map with both cluster centers and crime points"""
    sf_map = create_base_map(zoom=13)
    
    # add cluster centers
    for index, location in enumerate(mean_location_clusters):
        cluster_size = df_filtered[df_filtered['Cluster'] == index].shape[0]
        folium.Marker(
            location=[location[1], location[0]],
            popup=f"<b>Cluster {index}</b><br>{cluster_size} crimes",
            tooltip=f"Cluster {index}",
            icon=folium.Icon(color='red', icon='star', prefix='fa')
        ).add_to(sf_map)
    
    # add sample crime points
    for lat, lng, label in zip(df_incidents.Y[:500], 
                               df_incidents.X[:500], 
                               df_incidents.Category[:500]):
        folium.CircleMarker(
            [lat, lng],
            radius=2,
            color='blue',
            fill=True,
            popup=label,
            fill_color='lightblue',
            fill_opacity=0.4
        ).add_to(sf_map)
    
    return sf_map


def create_heat_map(df_heat, radius=15, blur=15, max_intensity=5):
    """create heat map showing crime density"""
    sf_heat_map = create_base_map()
    
    heat_data = [[row['Y'], row['X']] for idx, row in df_heat.iterrows()]
    
    HeatMap(
        heat_data,
        radius=radius,
        blur=blur,
        max_zoom=13,
        min_opacity=0.3,
        max_val=max_intensity
    ).add_to(sf_heat_map)
    
    return sf_heat_map

