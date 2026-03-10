# API Reference Guide

Quick reference for using the utilities and visualization modules.

## Utils Module (`utils.py`)

### DataLoader

```python
from utils import DataLoader

# Load a CSV file
df = DataLoader.load_data('client_data.csv')
# Returns: pd.DataFrame
# Raises: FileNotFoundError, ValueError
```

### DataValidator

```python
from utils import DataValidator

validator = DataValidator()

# Check for missing values
missing_info = validator.check_missing_values(df, threshold=0.5)
# Returns: {
#   'missing_count': pd.Series,
#   'missing_percent': pd.Series,
#   'critical_columns': list
# }

# Check for duplicates
n_dupes, pct_dupes = validator.check_duplicates(df)
# Returns: (int, float)

# Check data types
dtype_info = validator.check_data_types(df)
# Returns: {
#   'numeric_columns': list,
#   'categorical_columns': list,
#   'datetime_columns': list
# }
```

### DataProcessor

```python
from utils import DataProcessor

processor = DataProcessor()

# Convert datetime columns
df_dt = processor.convert_datetime_columns(
    df,
    columns=['date_col1', 'date_col2', ...]
)

# Remove outliers using IQR method
df_clean = processor.remove_outliers_iqr(
    df,
    column='numeric_column',
    multiplier=1.5  # Standard IQR multiplier
)

# Handle missing values
df_filled = processor.handle_missing_values(
    df,
    strategy='median',  # 'mean', 'median', 'forward_fill', 'drop'
    columns=['col1', 'col2']  # None = all columns with missing values
)
```

### FeatureEngineer

```python
from utils import FeatureEngineer

engineer = FeatureEngineer()

# Create price features
price_features = engineer.create_price_features(price_df)
# Returns: pd.DataFrame with engineered features
# Input required: columns named like 'price_p*_var', 'price_p*_fix'
```

### Convenience Functions

```python
from utils import load_and_validate

# Load and validate in one call
df = load_and_validate('data.csv')
# Automatically checks for missing values, duplicates, etc.
```

## Visualizer Module (`visualizer.py`)

### ChartConfig

```python
from visualizer import ChartConfig

# Quick access to chart configuration
ChartConfig.DEFAULT_FIGSIZE        # (12, 6)
ChartConfig.LARGE_FIGSIZE          # (18, 10)
ChartConfig.EXTRA_LARGE_FIGSIZE    # (18, 25)
ChartConfig.TITLE_FONTSIZE         # 14
ChartConfig.LABEL_FONTSIZE         # 12
ChartConfig.COLOR_PALETTE          # seaborn color palette
```

### Visualizer

```python
from visualizer import Visualizer
import matplotlib.pyplot as plt

# Plot stacked bars with annotations
fig = Visualizer.plot_stacked_bars(
    dataframe=df,
    title="Chart Title",
    figsize=(12, 6),
    rotation=45,
    legend_loc="upper right"
)
plt.show()  # or st.pyplot(fig) in Streamlit

# Plot distribution histogram
fig = Visualizer.plot_distribution(
    dataframe=df,
    column='column_name',
    figsize=(12, 6),
    bins=50
)

# Plot boxplots for multiple columns
fig = Visualizer.plot_boxplots(
    dataframe=df,
    columns=['col1', 'col2', 'col3'],
    figsize=(18, 10)
)

# Plot correlation heatmap
fig = Visualizer.plot_correlation_matrix(
    dataframe=df,
    figsize=(14, 12)
)

# Plot churn analysis
fig = Visualizer.plot_churn_analysis(client_df)

# Plot churn by categorical variable
fig = Visualizer.plot_categorical_churn(
    dataframe=df,
    column='channel_sales',
    figsize=(18, 10)
)
```

### QuickPlots

```python
from visualizer import QuickPlots

# Print summary statistics
QuickPlots.summary_statistics(df)

# Print data info
QuickPlots.data_info(df)

# Plot missing values
fig = QuickPlots.missing_values_plot(df)
```

## Config Module (`config.py`)

```python
from config import get_config

# Get all configurations
all_configs = get_config()

# Get specific section
data_config = get_config('data')
viz_config = get_config('visualization')
streamlit_config = get_config('streamlit')
analytics_config = get_config('analytics')

# Access specific settings
missing_threshold = data_config['missing_value_threshold']
figsize = viz_config['default_figsize']
cache_ttl = streamlit_config['cache_ttl']
```

## Common Workflows

### Complete Data Pipeline

```python
from utils import DataLoader, DataValidator, DataProcessor, FeatureEngineer
from visualizer import Visualizer
import matplotlib.pyplot as plt

# 1. Load data
client_df = DataLoader.load_data('client_data.csv')
price_df = DataLoader.load_data('price_data.csv')

# 2. Validate
validator = DataValidator()
missing_info = validator.check_missing_values(client_df)
dtype_info = validator.check_data_types(client_df)

# 3. Process
processor = DataProcessor()
client_df = processor.convert_datetime_columns(
    client_df,
    ['date_activ', 'date_end', 'date_modif_prod', 'date_renewal']
)

# 4. Engineer features
engineer = FeatureEngineer()
price_features = engineer.create_price_features(price_df)

# 5. Merge
merged = pd.merge(client_df, price_features, on='id')

# 6. Visualize
fig = Visualizer.plot_correlation_matrix(merged)
plt.show()

# 7. Export
merged.to_csv('output.csv', index=False)
```

### Quick Exploratory Analysis

```python
from utils import load_and_validate, DataValidator
from visualizer import Visualizer, QuickPlots
import matplotlib.pyplot as plt

# Load and validate
df = load_and_validate('data.csv')

# Quick summary
QuickPlots.summary_statistics(df)
QuickPlots.data_info(df)

# Visualizations
fig1 = QuickPlots.missing_values_plot(df)
fig2 = Visualizer.plot_churn_analysis(df)
fig3 = Visualizer.plot_distribution(df, 'consumption_column')

plt.show()
```

### In Streamlit App

```python
import streamlit as st
from utils import load_and_validate
from visualizer import Visualizer

# Load data
@st.cache_data
def load_data():
    return load_and_validate('data.csv')

df = load_data()

# Display title
st.title("Analysis Dashboard")

# Display visualization
fig = Visualizer.plot_correlation_matrix(df)
st.pyplot(fig)

# Display dataframe
st.dataframe(df.head())
```

## Error Handling

All functions include error handling with logging:

```python
import logging

# Logging is automatically configured
# Check logs for debug information

# In your code, you can also:
try:
    df = DataLoader.load_data('file.csv')
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Data error: {e}")
```

## Performance Tips

1. **Use caching in Streamlit**
```python
@st.cache_data
def expensive_operation(df):
    return df.groupby('category').sum()
```

2. **Sample large datasets**
```python
df_sample = df.sample(n=10000)  # Sample 10k rows
```

3. **Use categorical dtypes**
```python
df['category'] = df['category'].astype('category')
```

4. **Vectorize operations**
```python
# Instead of df.apply(lambda x: operation(x))
# Use df[column].str.method() or df[column].dt.method()
```

## Configuration Customization

Edit `config.py` to customize:

- **Figure sizes and fonts** in `VISUALIZATION_CONFIG`
- **Data processing thresholds** in `DATA_CONFIG`
- **Columns to analyze** in `ANALYTICS_CONFIG`
- **Export formats** in `EXPORT_CONFIG`

## Type Hints Reference

```python
# Common type hints used in the codebase
from typing import Tuple, Optional, List, Dict
import pandas as pd
import numpy as np

# Function signature examples
def function_name(
    df: pd.DataFrame,                    # DataFrame input
    column: str,                          # String input
    threshold: float = 0.5,              # Float with default
    figsize: Tuple[int, int] = (12, 6)  # Tuple type
) -> pd.DataFrame:                        # Return type
    pass

def optional_function(
    df: Optional[pd.DataFrame] = None    # Optional parameter
) -> Dict[str, List]:                    # Dict with typed values
    pass
```

---

**Last Updated**: March 2026  
**Version**: 1.0
