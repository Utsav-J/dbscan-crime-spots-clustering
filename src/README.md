# Source Code Directory

this directory contains the modular source code for the dbscan crime spots analysis application

## directory overview

```
src/
├── config/          configuration and settings
├── data/            data loading and processing
├── models/          machine learning models
├── pages/           streamlit page components
├── utils/           utility functions
└── visualization/   plotting and mapping functions
```

## quick navigation

**need to find something?**

- 🔧 **settings/config** → `config/settings.py`
- 📥 **load data** → `data/loader.py`
- 🔄 **process data** → `data/processor.py`
- 🤖 **dbscan algorithm** → `models/dbscan_model.py`
- 📄 **page modules** → `pages/*.py`
- 🎨 **ui components** → `utils/ui_helpers.py`
- 📊 **charts** → `visualization/plots.py`
- 🗺️ **maps** → `visualization/maps.py`

## module count

- **22 python files** (excluding `__init__.py`)
- **6 packages** (config, data, models, pages, utils, visualization)
- **8 page modules** (one for each app section)
- **~1,200 total lines** (down from 1,097 in one file)

## importing modules

all imports use the `src/` prefix:

```python
from src.config.settings import DEFAULT_EPS
from src.data.loader import load_crime_data
from src.models.dbscan_model import run_dbscan
from src.pages.home import render_home_page
from src.utils.ui_helpers import render_header
from src.visualization.plots import plot_crime_scatter
from src.visualization.maps import create_heat_map
```

## module responsibilities

### config/
centralizes all configuration, constants, and settings

### data/
handles data loading from remote sources and all data processing/transformation

### models/
contains the dbscan clustering implementation and related algorithms

### pages/
each file is a self-contained page module that renders a specific app section

### utils/
provides common utilities and ui helpers used across multiple pages

### visualization/
separates plotting logic (matplotlib/seaborn) and mapping logic (folium)

## code style

- **pep 8 compliant** - follows python style guidelines
- **informal docstrings** - conversational, human-readable
- **descriptive names** - self-documenting code
- **single responsibility** - each function does one thing well
- **dry principle** - no repeated code

## testing

modules are designed to be independently testable:

```python
# test a data processor
from src.data.processor import prepare_district_data

result = prepare_district_data(test_df)
assert 'Neighborhood' in result.columns
```

## adding new code

see `DEVELOPER_GUIDE.md` in the project root for detailed instructions on:
- adding new pages
- creating new visualizations
- adding data processing functions
- extending functionality

## architecture

see `ARCHITECTURE.md` in the project root for:
- detailed architecture documentation
- design principles
- data flow diagrams
- future improvement suggestions

## performance

- uses `@st.cache_data` for expensive operations
- efficient pandas vectorized operations
- sampling for large datasets
- lazy loading where possible

## dependencies

all dependencies are managed in `pyproject.toml` at the project root

