# Developer Quick Reference

quick reference for working with the modular codebase

## File Locations

### need to change a setting?
→ `src/config/settings.py`

### adding data processing logic?
→ `src/data/processor.py`

### need a new chart type?
→ `src/visualization/plots.py`

### adding a map visualization?
→ `src/visualization/maps.py`

### creating a new page?
→ `src/pages/your_page.py`

### adding reusable ui components?
→ `src/utils/ui_helpers.py`

### modifying dbscan logic?
→ `src/models/dbscan_model.py`

## Common Tasks

### task: add a new page

```python
# 1. create src/pages/my_page.py
from src.utils.ui_helpers import render_section_header

def render_my_page(df):
    """render my awesome new page"""
    render_section_header("My Page Title")
    # your code here
    st.write("Hello!")

# 2. update main.py
from src.pages.my_page import render_my_page

# add to page_routes dict:
"🎨 My Page": lambda: render_my_page(df)

# 3. update create_sidebar_navigation() in src/utils/ui_helpers.py
# add "🎨 My Page" to the radio options list
```

### task: add a new configuration value

```python
# src/config/settings.py
MY_NEW_SETTING = "some_value"

# use anywhere:
from src.config.settings import MY_NEW_SETTING
```

### task: add a new data processing function

```python
# src/data/processor.py
import streamlit as st

@st.cache_data  # if expensive operation
def process_my_data(df):
    """process data in some useful way"""
    # your logic here
    return processed_df
```

### task: create a new plot

```python
# src/visualization/plots.py
def plot_my_visualization(df):
    """create my custom plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # plotting code
    plt.tight_layout()
    return fig

# use in page:
from src.visualization.plots import plot_my_visualization
fig = plot_my_visualization(df)
st.pyplot(fig)
```

### task: create a new map type

```python
# src/visualization/maps.py
def create_my_map(df):
    """create custom folium map"""
    from src.config.settings import SF_LATITUDE, SF_LONGITUDE
    
    my_map = folium.Map(location=[SF_LATITUDE, SF_LONGITUDE])
    # add markers, layers, etc
    return my_map

# use in page:
from streamlit_folium import st_folium
from src.visualization.maps import create_my_map

my_map = create_my_map(df)
st_folium(my_map, width=1200, height=600)
```

## Import Patterns

```python
# configuration
from src.config.settings import SOME_SETTING

# data loading
from src.data.loader import load_crime_data, load_geojson

# data processing
from src.data.processor import (
    prepare_district_data,
    filter_by_category
)

# models
from src.models.dbscan_model import run_dbscan

# ui utilities
from src.utils.ui_helpers import (
    render_header,
    render_section_header
)

# visualizations
from src.visualization.plots import plot_crime_scatter
from src.visualization.maps import create_heat_map
```

## Code Style Guidelines

### docstrings - informal style

```python
def my_function(param1, param2):
    """
    short description of what this does
    
    longer explanation if needed, written casually
    like you're explaining to a colleague
    """
    pass
```

### naming conventions

```python
# use lowercase with underscores
def process_crime_data():
    pass

# descriptive variable names
crime_count = len(df)  # good
n = len(df)            # avoid

# constants in uppercase
DEFAULT_EPS = 0.020
```

### function organization

```python
# public functions first
def render_my_page(df):
    """main page render function"""
    _render_section_one(df)
    _render_section_two(df)

# private helper functions with leading underscore
def _render_section_one(df):
    """helper function for internal use"""
    pass
```

## Streamlit Caching

use caching for expensive operations:

```python
@st.cache_data
def expensive_computation(df):
    """this will only run once unless input changes"""
    # expensive processing
    return result
```

clear cache: press `c` in the streamlit app

## Testing Locally

```bash
# run the app
uv run streamlit run main.py

# with specific port
uv run streamlit run main.py --server.port 8502

# in headless mode
uv run streamlit run main.py --server.headless true
```

## Common Pitfalls

### pitfall: import errors

```python
# wrong - circular import
from main import something

# right - import from src modules
from src.data.loader import load_crime_data
```

### pitfall: modifying cached data

```python
# wrong - modifies cached dataframe
@st.cache_data
def load_data():
    return pd.read_csv(...)

df = load_data()
df['new_col'] = 1  # modifies cached data!

# right - copy first
df = load_data().copy()
df['new_col'] = 1  # safe
```

### pitfall: hardcoded values

```python
# wrong
latitude = 37.77

# right
from src.config.settings import SF_LATITUDE
latitude = SF_LATITUDE
```

## Debugging Tips

### print dataframe info

```python
st.write(df.head())
st.write(df.columns)
st.write(df.dtypes)
st.write(df.describe())
```

### inspect variables

```python
st.write(f"Debug: {variable_name}")
st.json({"key": "value"})
```

### check shapes and types

```python
st.write(f"Shape: {df.shape}")
st.write(f"Type: {type(some_object)}")
```

## Performance Tips

1. **use sampling** for large datasets in interactive components
2. **cache expensive operations** with `@st.cache_data`
3. **limit map markers** to reasonable numbers (< 2000)
4. **use efficient pandas operations** instead of loops
5. **avoid recomputing** same data multiple times

## module dependencies

```
main.py
├── config/settings.py
├── data/
│   ├── loader.py
│   └── processor.py
├── models/dbscan_model.py
├── pages/*.py
├── utils/ui_helpers.py
└── visualization/
    ├── plots.py
    └── maps.py
```

pages can import from any other module except other pages

## getting help

- **streamlit docs**: https://docs.streamlit.io
- **pandas docs**: https://pandas.pydata.org/docs/
- **scikit-learn docs**: https://scikit-learn.org/stable/
- **folium docs**: https://python-visualization.github.io/folium/

## checklist before committing

- [ ] code follows pep 8 style
- [ ] informal docstrings added
- [ ] no hardcoded magic numbers
- [ ] expensive operations are cached
- [ ] imports are organized
- [ ] functions have single responsibility
- [ ] tested locally with `streamlit run main.py`
- [ ] no linter errors

