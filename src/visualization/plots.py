"""
matplotlib and seaborn plotting functions
"""

import matplotlib.pyplot as plt
import seaborn as sns
from src.config.settings import CLUSTER_PALETTE


def plot_crime_scatter(df_sample, x_col='X', y_col='Y', alpha=0.35, size=12, 
                       title='Location of Crimes Reported in San Francisco'):
    """create scatter plot of crime locations"""
    fig, ax = plt.subplots(figsize=(size, size * 0.8))
    plt.title(title, loc='left', fontsize=16, fontweight='bold')
    sns.scatterplot(x=df_sample[x_col], y=df_sample[y_col], 
                   alpha=alpha, color='darkblue', s=10, ax=ax)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    plt.tight_layout()
    return fig


def plot_top_categories(category_counts, n=10):
    """plot top crime categories"""
    fig, ax = plt.subplots(figsize=(10, 6))
    category_counts.head(n).plot(kind='barh', ax=ax, color='steelblue')
    ax.set_xlabel('Number of Incidents')
    ax.set_title('Top 10 Crime Categories')
    plt.tight_layout()
    return fig


def plot_district_counts(district_counts):
    """plot incidents by police district"""
    fig, ax = plt.subplots(figsize=(10, 6))
    district_counts.plot(kind='barh', ax=ax, color='coral')
    ax.set_xlabel('Number of Incidents')
    ax.set_title('Incidents by Police District')
    plt.tight_layout()
    return fig


def plot_day_distribution(day_counts):
    """plot crime distribution by day of week"""
    fig, ax = plt.subplots(figsize=(10, 6))
    day_counts.plot(kind='bar', ax=ax, color='teal')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Number of Incidents')
    ax.set_title('Crime Distribution by Day')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_resolution_status(resolution_counts):
    """plot resolution status distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    resolution_counts.plot(kind='bar', ax=ax, color='purple')
    ax.set_xlabel('Resolution Type')
    ax.set_ylabel('Count')
    ax.set_title('Top 10 Resolution Types')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_clusters_with_noise(df_sample, labels):
    """plot dbscan clusters including noise points"""
    fig, ax = plt.subplots(figsize=(12, 10))
    scatter = sns.scatterplot(
        x=df_sample['X'], 
        y=df_sample['Y'], 
        hue=labels,
        palette=CLUSTER_PALETTE,
        alpha=0.4,
        s=15,
        ax=ax,
        legend='auto'
    )
    plt.title('Crime Spots in San Francisco - DBSCAN with Noise', 
             fontsize=16, fontweight='bold', loc='left')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
              title='Cluster', ncol=1)
    plt.tight_layout()
    return fig


def plot_clusters_without_noise(df_filtered, mean_location_clusters):
    """plot dbscan clusters without noise, labeled with cluster numbers"""
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.scatterplot(
        x=df_filtered['X'],
        y=df_filtered['Y'],
        hue=df_filtered['Cluster'],
        palette=CLUSTER_PALETTE,
        alpha=0.4,
        s=15,
        ax=ax,
        legend=None
    )
    
    # add cluster labels at centers
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
    return fig


def plot_cluster_sizes(df_filtered):
    """plot distribution of points per cluster"""
    fig, ax = plt.subplots(figsize=(10, 6))
    cluster_sizes = df_filtered['Cluster'].value_counts().sort_index()
    cluster_sizes.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_title('Points per Cluster')
    ax.set_xlabel('Cluster ID')
    ax.set_ylabel('Number of Points')
    plt.tight_layout()
    return fig


def plot_noise_distribution(n_clustered, n_noise):
    """plot pie chart of clustered vs noise points"""
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ['Clustered Points', 'Noise Points']
    sizes = [n_clustered, n_noise]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
          colors=['lightgreen', 'lightcoral'])
    ax.set_title('Clustered vs Noise Points')
    return fig


def plot_district_bar_chart(df_san_sorted):
    """plot crime count by district as bar chart"""
    fig, ax = plt.subplots(figsize=(8, 6))
    df_san_sorted.plot(x='Neighborhood', y='Count', kind='bar', 
                      ax=ax, color='orangered', legend=False)
    ax.set_title('Crime Count by District')
    ax.set_xlabel('District')
    ax.set_ylabel('Number of Incidents')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

