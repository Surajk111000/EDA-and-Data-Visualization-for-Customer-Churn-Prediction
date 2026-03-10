"""
Configuration file for the EDA Dashboard
Modify these settings to customize the application behavior
"""

# ==================== DATA SETTINGS ====================
DATA_CONFIG = {
    # Input files
    "client_data_path": "./client_data.csv",
    "price_data_path": "./price_data.csv",
    
    # Output files
    "output_data_path": "./clean_data_after_eda.csv",
    
    # Data processing settings
    "missing_value_threshold": 0.5,  # 50% threshold
    "missing_value_strategy": "mean",  # 'mean', 'median', 'forward_fill', 'drop'
    "outlier_multiplier": 1.5,  # IQR multiplier for outlier detection
    
    # Datetime columns to convert
    "datetime_columns": [
        "date_activ",
        "date_end",
        "date_modif_prod",
        "date_renewal"
    ],
    
    # Price aggregation date ranges (YYYY-MM-DD)
    "price_periods": {
        "year": None,  # All data
        "6m": "2015-06-01",
        "3m": "2015-10-01"
    }
}

# ==================== VISUALIZATION SETTINGS ====================
VISUALIZATION_CONFIG = {
    # Figure sizes
    "default_figsize": (12, 6),
    "large_figsize": (18, 10),
    "extra_large_figsize": (18, 25),
    
    # Font sizes
    "title_fontsize": 14,
    "label_fontsize": 12,
    "annotation_fontsize": 11,
    
    # Colors
    "color_scheme": "husl",  # Color palette: 'husl', 'Set2', 'husl', etc.
    "churn_color": "#e74c3c",  # Red for churn
    "retention_color": "#2ecc71",  # Green for retention
    
    # Plot settings
    "plot_style": "whitegrid",  # seaborn style
    "use_annotations": True,
    "grid_enabled": True,
    "legend_location": "upper right"
}

# ==================== STREAMLIT SETTINGS ====================
STREAMLIT_CONFIG = {
    # Page configuration
    "page_title": "EDA - Customer Churn Analysis",
    "page_icon": "📊",
    "layout": "wide",  # 'wide' or 'centered'
    "initial_sidebar_state": "expanded",
    
    # Caching settings
    "enable_caching": True,
    "cache_ttl": 3600,  # Cache timeout in seconds (1 hour)
    
    # Performance settings
    "sample_data": False,  # Set to True for large datasets
    "sample_size": 10000,  # Number of rows to sample
    
    # UI Settings
    "show_debug_info": False,
    "show_data_types": True,
    "show_memory_usage": True,
    "download_formats": ["csv", "excel"]
}

# ==================== ANALYTICS SETTINGS ====================
ANALYTICS_CONFIG = {
    # Churn definition
    "churn_column": "churn",
    "churn_value": 1,  # Value that represents churned customer
    
    # Analysis features
    "analyze_consumption": True,
    "analyze_price_sensitivity": True,
    "analyze_categorical": True,
    "analyze_correlations": True,
    
    # Specific columns to analyze
    "consumption_columns": [
        "cons_12m",
        "cons_gas_12m",
        "cons_last_month",
        "imp_cons"
    ],
    
    "forecast_columns": [
        "forecast_cons_12m",
        "forecast_cons_year",
        "forecast_discount_energy",
        "forecast_meter_rent_12m",
        "forecast_price_energy_p1",
        "forecast_price_energy_p2",
        "forecast_price_pow_p1"
    ],
    
    "categorical_columns": [
        "channel_sales",
        "has_gas",
        "origin_up"
    ]
}

# ==================== LOGGING SETTINGS ====================
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": "./logs/app.log",
    "enable_file_logging": False
}

# ==================== FEATURE ENGINEERING ====================
FEATURE_CONFIG = {
    # Price feature aggregation
    "create_price_features": True,
    "price_components": ["_var", "_fix"],  # Variable and fixed components
    
    # Summary statistics to create
    "create_consumption_ratios": True,
    "create_temporal_features": True,
    
    # Interaction features
    "create_interaction_features": False,
    "interaction_pairs": ["cons_12m", "pow_max"]  # Example pairs
}

# ==================== EXPORT SETTINGS ====================
EXPORT_CONFIG = {
    # Export formats
    "csv_enabled": True,
    "excel_enabled": True,
    "parquet_enabled": False,  # Requires pyarrow
    
    # CSV options
    "csv_index": False,
    
    # Excel options
    "excel_engine": "openpyxl",
    "excel_sheet_name": "Data",
    
    # Default filename
    "default_filename": "processed_churn_data"
}

# ==================== ADVANCED SETTINGS ====================
ADVANCED_CONFIG = {
    # Data validation
    "strict_validation": False,  # Raise errors vs warnings
    "check_duplicates": True,
    "check_missing_values": True,
    "check_data_types": True,
    
    # Performance optimization
    "use_categorical_dtype": True,
    "optimize_dtypes": False,  # Compress numeric types
    
    # Security
    "sanitize_filenames": True,
    "max_file_size_mb": 500
}

def get_config(section: str = None):
    """
    Get configuration dictionary
    
    Args:
        section: Specific section ('data', 'viz', 'streamlit', etc.)
                If None, returns all configs
    
    Returns:
        Configuration dictionary
    """
    all_configs = {
        "data": DATA_CONFIG,
        "visualization": VISUALIZATION_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "analytics": ANALYTICS_CONFIG,
        "logging": LOGGING_CONFIG,
        "features": FEATURE_CONFIG,
        "export": EXPORT_CONFIG,
        "advanced": ADVANCED_CONFIG
    }
    
    if section is None:
        return all_configs
    
    return all_configs.get(section, {})


if __name__ == "__main__":
    # Print all configurations
    import json
    configs = get_config()
    for section, config in configs.items():
        print(f"\n{section.upper()}")
        print("=" * 50)
        print(json.dumps(config, indent=2))
