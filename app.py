"""
Streamlit EDA App for Customer Churn Prediction
A comprehensive exploratory data analysis dashboard
"""
import streamlit as st
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from utils import DataLoader, DataValidator, DataProcessor, FeatureEngineer, load_and_validate
from visualizer import Visualizer, QuickPlots, ChartConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="EDA - Customer Churn Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """Load data with caching"""
    try:
        df = load_and_validate(filepath)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


@st.cache_data
def process_data(client_df: pd.DataFrame, price_df: pd.DataFrame) -> dict:
    """Process and merge data"""
    try:
        processor = DataProcessor()
        
        # Convert datetime columns
        date_cols = ["date_activ", "date_end", "date_modif_prod", "date_renewal"]
        client_df_processed = processor.convert_datetime_columns(client_df, date_cols)
        
        # Create price features
        engineer = FeatureEngineer()
        price_features = engineer.create_price_features(price_df)
        
        # Merge datasets
        merged_df = pd.merge(client_df_processed.drop(columns=['churn']), 
                            price_features, on='id', how='inner')
        
        # Add churn back
        merged_df = pd.merge(merged_df, client_df_processed[['id', 'churn']], 
                            on='id', how='left')
        
        return {
            'client_df': client_df_processed,
            'price_df': price_df,
            'price_features': price_features,
            'merged_df': merged_df
        }
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None


def display_header():
    """Display app header"""
    st.title("📊 Customer Churn Prediction - EDA Dashboard")
    st.markdown("""
    A comprehensive Exploratory Data Analysis platform for understanding customer churn patterns.
    Navigate through different sections using the sidebar to explore the data.
    """)


def display_data_overview(client_df: pd.DataFrame, price_df: pd.DataFrame):
    """Display data overview section"""
    st.header("📋 Data Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(client_df))
    
    with col2:
        st.metric("Price Records", len(price_df))
    
    with col3:
        churn_count = client_df['churn'].sum()
        st.metric("Churned Customers", int(churn_count))
    
    with col4:
        churn_rate = (client_df['churn'].sum() / len(client_df)) * 100
        st.metric("Churn Rate", f"{churn_rate:.2f}%")
    
    st.divider()
    
    # Data quality checks
    st.subheader("🔍 Data Quality Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Client Data**")
        validator = DataValidator()
        missing_info = validator.check_missing_values(client_df)
        n_dup, pct_dup = validator.check_duplicates(client_df)
        
        st.write(f"- Shape: {client_df.shape}")
        st.write(f"- Duplicate rows: {n_dup} ({pct_dup:.2f}%)")
        st.write(f"- Columns with missing values: {len(missing_info['critical_columns'])}")
        
        if st.checkbox("Show missing values details"):
            st.dataframe(missing_info['missing_percent'][missing_info['missing_percent'] > 0])
    
    with col2:
        st.write("**Price Data**")
        missing_info_price = validator.check_missing_values(price_df)
        n_dup_price, pct_dup_price = validator.check_duplicates(price_df)
        
        st.write(f"- Shape: {price_df.shape}")
        st.write(f"- Duplicate rows: {n_dup_price} ({pct_dup_price:.2f}%)")
        st.write(f"- Columns with missing values: {len(missing_info_price['critical_columns'])}")


def display_statistical_summary(client_df: pd.DataFrame):
    """Display statistical summary"""
    st.header("📈 Statistical Summary")
    
    tab1, tab2, tab3 = st.tabs(["Descriptive Stats", "Data Types", "Missing Values"])
    
    with tab1:
        st.subheader("Descriptive Statistics")
        st.dataframe(client_df.describe(), use_container_width=True)
    
    with tab2:
        st.subheader("Data Types Distribution")
        
        validator = DataValidator()
        dtype_info = validator.check_data_types(client_df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Numeric Columns:** {len(dtype_info['numeric_columns'])}")
            if st.checkbox("Show numeric columns"):
                st.write(dtype_info['numeric_columns'])
        
        with col2:
            st.write(f"**Categorical Columns:** {len(dtype_info['categorical_columns'])}")
            if st.checkbox("Show categorical columns"):
                st.write(dtype_info['categorical_columns'])
        
        with col3:
            st.write(f"**DateTime Columns:** {len(dtype_info['datetime_columns'])}")
            if st.checkbox("Show datetime columns"):
                st.write(dtype_info['datetime_columns'])
    
    with tab3:
        st.subheader("Missing Values Analysis")
        validator = DataValidator()
        missing = validator.check_missing_values(client_df)
        missing_df = pd.DataFrame({
            'Column': client_df.columns,
            'Missing Count': missing['missing_count'],
            'Missing %': missing['missing_percent']
        }).sort_values('Missing %', ascending=False)
        missing_df = missing_df[missing_df['Missing %'] > 0]
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True)
            fig = QuickPlots.missing_values_plot(client_df)
            st.pyplot(fig)
        else:
            st.success("✅ No missing values found!")


def display_churn_analysis(client_df: pd.DataFrame):
    """Display churn analysis"""
    st.header("🎯 Churn Analysis")
    
    # Overall churn statistics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    
    total_customers = len(client_df)
    churned = client_df['churn'].sum()
    retained = total_customers - churned
    
    with col1:
        st.metric("Churned", int(churned))
    with col2:
        st.metric("Retained", int(retained))
    with col3:
        st.metric("Churn Rate", f"{(churned/total_customers)*100:.2f}%")
    
    st.divider()
    
    # Churn by categorical variables
    st.subheader("Churn by Category")
    
    categorical_cols = client_df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols = [col for col in categorical_cols if col != 'id']
    
    if categorical_cols:
        selected_col = st.selectbox("Select categorical variable:", categorical_cols)
        
        if selected_col:
            try:
                fig = Visualizer.plot_categorical_churn(client_df, selected_col)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error plotting: {str(e)}")


def display_consumption_analysis(client_df: pd.DataFrame):
    """Display consumption analysis"""
    st.header("⚡ Consumption Analysis")
    
    consumption_cols = ['cons_12m', 'cons_gas_12m', 'cons_last_month', 'imp_cons']
    available_cols = [col for col in consumption_cols if col in client_df.columns]
    
    if not available_cols:
        st.warning("Consumption columns not found in the dataset")
        return
    
    st.subheader("Distribution Analysis")
    
    selected_col = st.selectbox("Select consumption variable:", available_cols)
    
    if selected_col:
        try:
            fig = Visualizer.plot_distribution(client_df, selected_col)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error plotting: {str(e)}")
    
    st.divider()
    st.subheader("Outlier Detection")
    
    fig = Visualizer.plot_boxplots(client_df, available_cols, 
                                  figsize=ChartConfig.LARGE_FIGSIZE)
    st.pyplot(fig)


def display_correlation_analysis(merged_df: pd.DataFrame):
    """Display correlation analysis"""
    st.header("🔗 Correlation Analysis")
    
    st.subheader("Price Sensitivity Analysis")
    
    # Select numeric columns
    numeric_cols = merged_df.select_dtypes(include=[np.number]).columns.tolist()
    
    if 'churn' in numeric_cols:
        numeric_cols.remove('churn')
    
    # Limit columns for visualization
    if len(numeric_cols) > 30:
        st.info(f"📊 Showing correlation for a subset of features (30/{len(numeric_cols)})")
        selected_cols = numeric_cols[:30] + ['churn']
    else:
        selected_cols = numeric_cols + ['churn'] if 'churn' in merged_df.columns else numeric_cols
    
    try:
        subset_df = merged_df[selected_cols]
        fig = Visualizer.plot_correlation_matrix(subset_df)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error plotting correlation: {str(e)}")


def display_data_preview(merged_df: pd.DataFrame):
    """Display data preview"""
    st.header("👁️ Data Preview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        n_rows = st.slider("Number of rows to display:", 5, 100, 20)
    
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    st.dataframe(merged_df.head(n_rows), use_container_width=True)
    
    st.divider()
    st.subheader("Dataset Info")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Total Rows:** {len(merged_df)}")
        st.write(f"**Total Columns:** {len(merged_df.columns)}")
    
    with col2:
        st.write(f"**Memory Usage:** {merged_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        st.write(f"**Data Types:** {merged_df.dtypes.nunique()}")


def display_export_options(merged_df: pd.DataFrame):
    """Display export options"""
    st.header("💾 Export Data")
    
    st.subheader("Download Processed Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = merged_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="processed_churn_data.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = pd.ExcelWriter('processed_data.xlsx', engine='openpyxl')
        merged_df.to_excel(excel_buffer, sheet_name="Data")
        
        # Get the buffer
        try:
            with open('processed_data.xlsx', 'rb') as f:
                excel_data = f.read()
            
            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name="processed_churn_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.warning("Excel export not available")


def main():
    """Main application"""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio(
        "Select Section:",
        [
            "📋 Overview",
            "📈 Statistical Summary",
            "🎯 Churn Analysis",
            "⚡ Consumption Analysis",
            "🔗 Correlation Analysis",
            "👁️ Data Preview",
            "💾 Export Data",
            "ℹ️ About"
        ]
    )
    
    st.sidebar.divider()
    st.sidebar.write("**Data Files Location:**")
    st.sidebar.write("```")
    st.sidebar.write(Path.cwd())
    st.sidebar.write("```")
    
    # Load data
    try:
        client_df = load_data('./client_data.csv')
        price_df = load_data('./price_data.csv')
        
        if client_df is None or price_df is None:
            st.error("Failed to load data files")
            return
        
        # Process data
        processed_data = process_data(client_df, price_df)
        if processed_data is None:
            return
        
        merged_df = processed_data['merged_df']
        
        # Route to selected page
        if page == "📋 Overview":
            display_data_overview(client_df, price_df)
        
        elif page == "📈 Statistical Summary":
            display_statistical_summary(client_df)
        
        elif page == "🎯 Churn Analysis":
            display_churn_analysis(client_df)
        
        elif page == "⚡ Consumption Analysis":
            display_consumption_analysis(client_df)
        
        elif page == "🔗 Correlation Analysis":
            display_correlation_analysis(merged_df)
        
        elif page == "👁️ Data Preview":
            display_data_preview(merged_df)
        
        elif page == "💾 Export Data":
            display_export_options(merged_df)
        
        elif page == "ℹ️ About":
            display_about()
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Error in main: {str(e)}")


def display_about():
    """Display about section"""
    st.header("ℹ️ About")
    
    st.markdown("""
    ### Customer Churn Prediction EDA Dashboard
    
    This dashboard provides comprehensive exploratory data analysis for customer churn prediction.
    
    **Key Features:**
    - 📊 Statistical summaries and data quality checks
    - 🎯 Churn analysis by various dimensions
    - ⚡ Consumption pattern visualization
    - 🔗 Correlation analysis for feature relationships
    - 💾 Data export capabilities
    
    **Technology Stack:**
    - **Python**: Data processing and analysis
    - **Streamlit**: Interactive web dashboard
    - **Pandas**: Data manipulation
    - **Matplotlib & Seaborn**: Visualizations
    - **Scikit-learn**: Machine learning utilities
    
    **Data Processing:**
    - Automated datetime conversion
    - Price feature engineering
    - Data validation and quality checks
    - Outlier detection and handling
    
    **Usage:**
    1. Ensure `client_data.csv` and `price_data.csv` are in the working directory
    2. Run: `streamlit run app.py`
    3. Navigate through sections using the sidebar
    
    **Version**: 1.0  
    **Last Updated**: March 2026
    """)
    
    st.divider()
    
    st.subheader("📚 Documentation")
    
    with st.expander("Data Schema"):
        st.markdown("""
        **Client Data Columns:**
        - `id`: Unique customer identifier
        - `churn`: Target variable (0=retained, 1=churned)
        - `channel_sales`: Sales channel
        - `cons_12m`, `cons_gas_12m`: Consumption metrics
        - `has_gas`: Whether customer uses gas (t/f)
        - `pow_max`: Maximum power subscribed
        - `nb_prod_act`: Number of active products
        - `num_years_antig`: Customer tenure
        - `margin_*`: Margin metrics
        - `forecast_*`: Forecasted metrics
        - Date columns: Various transaction/modification dates
        
        **Price Data Columns:**
        - `id`: Customer identifier
        - `price_date`: Date of price record
        - `price_p*_var`: Variable price component
        - `price_p*_fix`: Fixed price component
        """)
    
    with st.expander("Methodology"):
        st.markdown("""
        This EDA follows these steps:
        
        1. **Data Loading**: Load and validate CSV files
        2. **Data Profiling**: Assess quality, types, and missing values
        3. **Datetime Processing**: Convert date strings to datetime objects
        4. **Feature Engineering**: Create derived features from price data
        5. **Exploratory Analysis**: Visualize distributions, relationships, and patterns
        6. **Correlation Analysis**: Identify relationships with churn
        7. **Export**: Enable processed data download
        """)


if __name__ == "__main__":
    main()
