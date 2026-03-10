# Customer Churn Prediction - EDA Dashboard

A professional, production-ready Exploratory Data Analysis (EDA) dashboard for customer churn prediction built with Streamlit.

## 📁 Project Structure

```
.
├── app.py                          # Main Streamlit application
├── utils.py                        # Data processing utilities
├── visualizer.py                   # Visualization functions
├── requirements.txt                # Python dependencies
├── client_data.csv                 # Client data file
├── price_data.csv                  # Price data file
├── clean_data_after_eda.csv       # Output - processed data
└── README.md                       # This file
```

## 🎯 Features

### Data Processing & Validation
- ✅ Automated data loading with error handling
- ✅ Data quality assessment (missing values, duplicates, data types)
- ✅ Datetime conversion and normalization
- ✅ Feature engineering for price sensitivity analysis
- ✅ Outlier detection using IQR method
- ✅ Missing value imputation strategies

### Visualizations
- 📊 Stacked bar charts with annotations
- 📈 Distribution histograms
- 📦 Boxplots for outlier detection
- 🔥 Correlation heatmaps
- 🎯 Categorical churn analysis
- 📋 Missing values visualization

### Interactive Dashboard
- 🔍 Multi-section navigation
- 📋 Data overview with quality metrics
- 📈 Statistical summaries and distribution analysis
- 🎯 Comprehensive churn analysis
- ⚡ Consumption pattern exploration
- 🔗 Feature correlation analysis
- 👁️ Data preview with filtering
- 💾 Export capabilities (CSV, Excel)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Installation

1. **Navigate to project directory:**
   ```bash
   cd path/to/EDA-and-Data-Visualization-for-Customer-Churn-Prediction
   ```

2. **Create virtual environment (recommended):**
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
   
   **macOS/Linux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Using Streamlit directly**
```bash
streamlit run app.py
```

**Option 2: Using Python module**
```bash
python -m streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Using the Dashboard

### Navigation
Use the sidebar to navigate between different sections:

- **📋 Overview**: Quick statistics and data quality checks
- **📈 Statistical Summary**: Descriptive statistics, data types, missing values
- **🎯 Churn Analysis**: Overall churn metrics and categorical breakdowns
- **⚡ Consumption Analysis**: Consumption patterns and distributions
- **🔗 Correlation Analysis**: Feature relationships and price sensitivity
- **👁️ Data Preview**: Browse and inspect the processed data
- **💾 Export Data**: Download processed data as CSV/Excel
- **ℹ️ About**: Documentation and methodology

### Key Insights

The dashboard provides insights into:

1. **Churn Patterns**: Identify which customer segments have higher churn rates
2. **Consumption Behavior**: Understand consumption patterns by churn status
3. **Price Sensitivity**: Analyze price-related features and their correlation with churn
4. **Data Quality**: Ensure data integrity before modeling
5. **Feature Relationships**: Identify multicollinearity and feature importance

## 📈 Module Overview

### `utils.py`
Core data processing and validation utilities:

- **DataLoader**: Load CSV files with error handling
- **DataValidator**: Check data quality, missing values, duplicates
- **DataProcessor**: Handle datetime conversion, outliers, missing values
- **FeatureEngineer**: Create derived features (price sensitivity metrics)

```python
from utils import DataLoader, DataValidator, FeatureEngineer

# Load data
df = DataLoader.load_data('client_data.csv')

# Validate data
validator = DataValidator()
missing_info = validator.check_missing_values(df)

# Engineer features
engineer = FeatureEngineer()
features = engineer.create_price_features(price_df)
```

### `visualizer.py`
Professional visualization functions:

- **Visualizer**: Main class for all plots
- **ChartConfig**: Configuration for colors, sizes, fonts
- **QuickPlots**: Helper functions for exploratory plots

```python
from visualizer import Visualizer

# Plot distribution
fig = Visualizer.plot_distribution(df, 'column_name')

# Plot correlation
fig = Visualizer.plot_correlation_matrix(df)

# Plot stacked bars
fig = Visualizer.plot_stacked_bars(data, 'Chart Title')
```

### `app.py`
Streamlit application with interactive dashboard

## 🔧 Configuration

### Modify Chart Defaults
Edit `ChartConfig` in `visualizer.py`:

```python
class ChartConfig:
    DEFAULT_FIGSIZE = (12, 6)
    LARGE_FIGSIZE = (18, 10)
    TITLE_FONTSIZE = 14
    LABEL_FONTSIZE = 12
    COLOR_PALETTE = sns.color_palette("husl", 8)
```

### Adjust Data Processing
Modify parameters in data processing functions:

```python
# Handle missing values
df = DataProcessor.handle_missing_values(
    df, 
    strategy='median',  # 'mean', 'median', 'forward_fill', 'drop'
    columns=['column1', 'column2']
)

# Remove outliers
df_clean = DataProcessor.remove_outliers_iqr(
    df, 
    column='numeric_column',
    multiplier=1.5  # Standard is 1.5
)
```

## 📝 Code Improvements from Original Notebook

### ✅ What's Been Improved

1. **Modularity**: Code split into logical components (utils, visualizer, app)
2. **Error Handling**: Comprehensive try-except blocks with logging
3. **Reusability**: Functions and classes for DRY principle
4. **Documentation**: Docstrings for all functions and classes
5. **Type Hints**: Type annotations for better IDE support
6. **Validation**: Data quality checks before processing
7. **Caching**: Streamlit caching for performance
8. **Logging**: Structured logging for debugging
9. **Configuration**: Centralized config for customization
10. **Testing Ready**: Clean code structure for unit testing

### 📊 Original vs Improved

| Aspect | Original | Improved |
|--------|----------|----------|
| Structure | Monolithic notebook | Modular architecture |
| Error Handling | Minimal | Comprehensive |
| Reusability | Limited | High |
| Documentation | Sparse | Complete |
| Type Hints | None | Full coverage |
| Testing | Difficult | Easy |
| Deployment | Local only | Streamlit ready |
| Logging | Print statements | Structured logging |
| Code Organization | Linear | Object-oriented |
| Maintainability | Low | High |

## 🐛 Troubleshooting

### Issue: "FileNotFoundError: File not found"
**Solution**: Ensure `client_data.csv` and `price_data.csv` are in the same directory as `app.py`

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port 8501 is already in use"
**Solution**: Run on different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow performance with large datasets
**Solution**: The app uses Streamlit caching by default. For very large files:
- Consider data sampling
- Increase cache timeout:
  ```python
  @st.cache_data(ttl=3600)  # 1 hour cache
  ```

## 📦 Dependencies

- **streamlit**: Web app framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **matplotlib**: Static plotting
- **seaborn**: Statistical visualization
- **scikit-learn**: Machine learning utilities
- **openpyxl**: Excel file support

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t churn-eda .
docker run -p 8501:8501 churn-eda
```

### AWS/Azure Deployment
- Use EC2 or App Service
- Install Python and dependencies
- Run Streamlit with proper configuration

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Guide](https://matplotlib.org/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

## 🤝 Contributing

To extend the dashboard:

1. Add new functions to respective modules
2. Follow existing code style and documentation
3. Add type hints and docstrings
4. Test thoroughly before deploying

## 📄 License

This project is open source and available for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the documentation
3. Check Streamlit forums and Stack Overflow

---

**Last Updated**: March 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
