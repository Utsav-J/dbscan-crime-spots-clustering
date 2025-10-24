# Architecture Documentation

## Overview

this is a modular streamlit application for crime spot detection using the dbscan clustering algorithm. the codebase is organized for maintainability, readability, and scalability.

## Design Principles

1. **separation of concerns** - each module has a single, well-defined responsibility
2. **modularity** - components are loosely coupled and easily replaceable
3. **reusability** - common functionality is extracted into utility functions
4. **scalability** - easy to add new features or pages
5. **testability** - isolated components can be tested independently

## Directory Structure

```
src/
├── config/          # configuration and constants
├── data/            # data loading and processing
├── models/          # machine learning models
├── pages/           # streamlit page components
├── utils/           # utility functions
└── visualization/   # plotting and mapping
```

## Module Responsibilities

### config/

centralizes all configuration settings and constants to avoid magic numbers and hardcoded values throughout the codebase.

**settings.py**
- data source urls
- default parameters for algorithms
- ui styling and theming
- map configuration defaults

### data/

handles all data-related operations including loading, caching, and transformation.

**loader.py**
- loads crime dataset from remote source
- loads geojson boundary data
- provides sampling utilities
- uses streamlit caching for performance

**processor.py**
- aggregates data by various dimensions
- filters data by criteria
- calculates cluster statistics
- transforms data for visualization

### models/

contains machine learning model implementations and related utilities.

**dbscan_model.py**
- runs dbscan clustering algorithm
- normalizes geographic coordinates
- calculates clustering metrics
- provides quality assessment functions

### pages/

each page is a self-contained module that renders a specific section of the app.

**home.py** - landing page with overview and quick stats

**theory.py** - educational content about dbscan algorithm

**dataset_overview.py** - interactive dataset exploration

**data_visualization.py** - scatter plots and choropleth maps

**dbscan_clustering.py** - interactive parameter tuning

**interactive_maps.py** - various folium map visualizations

**heat_maps.py** - density-based crime visualization

**summary.py** - key findings and recommendations

### utils/

provides common utilities used across multiple modules.

**ui_helpers.py**
- consistent header rendering
- metric display utilities
- navigation menu creation
- reusable ui components

### visualization/

separates plotting logic from business logic for cleaner code.

**plots.py**
- matplotlib and seaborn plotting functions
- scatter plots, bar charts, pie charts
- cluster visualizations
- consistent styling and formatting

**maps.py**
- folium map creation
- choropleth maps
- marker maps and clustering
- heat maps
- reusable map components

## Data Flow

```
main.py
  ↓
load_crime_data() [data/loader.py]
  ↓
create_sidebar_navigation() [utils/ui_helpers.py]
  ↓
route to page [pages/*.py]
  ↓
process data [data/processor.py]
  ↓
run model [models/dbscan_model.py] (if needed)
  ↓
create visualizations [visualization/plots.py or maps.py]
  ↓
render to streamlit
```

## Adding New Features

### adding a new page

1. create new file in `src/pages/` (e.g., `my_new_page.py`)
2. implement `render_my_new_page(df)` function
3. import in `main.py`
4. add route in `page_routes` dictionary
5. add menu item in `create_sidebar_navigation()`

### adding new visualization

1. add function to `src/visualization/plots.py` or `maps.py`
2. follow existing naming conventions
3. return figure object (matplotlib or folium)
4. use configuration from `settings.py`

### adding new data processing

1. add function to `src/data/processor.py`
2. use `@st.cache_data` decorator if appropriate
3. document parameters and return values
4. keep functions focused and single-purpose

## Performance Optimization

- **caching**: uses `@st.cache_data` for expensive operations
- **sampling**: provides user controls for sample sizes
- **lazy loading**: only processes data when needed
- **efficient data structures**: uses pandas for vectorized operations

## Code Style

- **pep 8 compliant**: follows python style guidelines
- **informal docstrings**: human-readable, conversational style
- **lowercase naming**: consistent naming conventions
- **descriptive names**: clear, self-documenting code
- **comments**: explain why, not what

## Testing Strategy

components can be tested independently:

```python
# example: test data processor
from src.data.processor import prepare_district_data
import pandas as pd

# mock data
df = pd.DataFrame({...})
result = prepare_district_data(df)
assert 'Neighborhood' in result.columns
```

## Dependencies

see `pyproject.toml` for complete dependency list. key dependencies:

- streamlit: web framework
- pandas: data manipulation
- scikit-learn: machine learning
- folium: interactive maps
- matplotlib/seaborn: plotting

## Running the Application

```bash
# install dependencies
uv sync

# run the app
uv run streamlit run main.py
```

## Troubleshooting

**import errors**: ensure all `__init__.py` files are present

**caching issues**: clear streamlit cache with `c` key in browser

**memory issues**: reduce sample sizes in configuration

**map loading errors**: check internet connection for geojson

## Contributing

when contributing:

1. follow existing code organization
2. maintain informal docstring style
3. add comments for complex logic
4. test changes before committing
5. update documentation as needed

