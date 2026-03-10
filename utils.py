"""
Utility functions for data processing and analysis
"""
import logging
from typing import Tuple, Optional
import pandas as pd
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and validate data files"""
    
    @staticmethod
    def load_data(filepath: str) -> pd.DataFrame:
        """
        Load CSV file with error handling
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file is empty or corrupted
        """
        try:
            if not Path(filepath).exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            df = pd.read_csv(filepath)
            
            if df.empty:
                raise ValueError(f"File is empty: {filepath}")
            
            logger.info(f"Successfully loaded {filepath} with shape {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading {filepath}: {str(e)}")
            raise


class DataValidator:
    """Validate data quality and integrity"""
    
    @staticmethod
    def check_missing_values(df: pd.DataFrame, threshold: float = 0.5) -> dict:
        """
        Check for missing values in DataFrame
        
        Args:
            df: DataFrame to check
            threshold: Maximum allowed percentage of missing values (0-1)
            
        Returns:
            Dictionary with missing value information
        """
        missing_info = {
            'missing_count': df.isnull().sum(),
            'missing_percent': (df.isnull().sum() / len(df)) * 100,
            'critical_columns': []
        }
        
        for col in df.columns:
            if missing_info['missing_percent'][col] > threshold * 100:
                missing_info['critical_columns'].append(col)
        
        return missing_info
    
    @staticmethod
    def check_duplicates(df: pd.DataFrame) -> Tuple[int, float]:
        """
        Check for duplicate rows
        
        Args:
            df: DataFrame to check
            
        Returns:
            Tuple of (number of duplicates, percentage of duplicates)
        """
        n_duplicates = df.duplicated().sum()
        pct_duplicates = (n_duplicates / len(df)) * 100
        return n_duplicates, pct_duplicates
    
    @staticmethod
    def check_data_types(df: pd.DataFrame) -> dict:
        """
        Check data types in DataFrame
        
        Args:
            df: DataFrame to check
            
        Returns:
            Dictionary with data type information
        """
        return {
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
        }


class DataProcessor:
    """Process and transform data"""
    
    @staticmethod
    def convert_datetime_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Convert specified columns to datetime format
        
        Args:
            df: DataFrame
            columns: List of column names to convert
            
        Returns:
            DataFrame with converted datetime columns
        """
        df = df.copy()
        for col in columns:
            try:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
            except Exception as e:
                logger.warning(f"Could not convert {col} to datetime: {str(e)}")
        return df
    
    @staticmethod
    def remove_outliers_iqr(df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers using Interquartile Range (IQR) method
        
        Args:
            df: DataFrame
            column: Column to check for outliers
            multiplier: IQR multiplier (default 1.5)
            
        Returns:
            DataFrame without outliers
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean', 
                            columns: Optional[list] = None) -> pd.DataFrame:
        """
        Handle missing values in DataFrame
        
        Args:
            df: DataFrame
            strategy: Strategy to use ('mean', 'median', 'forward_fill', 'drop')
            columns: Specific columns to process (None = all columns with missing values)
            
        Returns:
            DataFrame with missing values handled
        """
        df = df.copy()
        
        if columns is None:
            columns = df.columns[df.isnull().any()].tolist()
        
        for col in columns:
            if df[col].isnull().sum() > 0:
                if strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif strategy == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif strategy == 'forward_fill':
                    df[col].fillna(method='ffill', inplace=True)
                elif strategy == 'drop':
                    df.dropna(subset=[col], inplace=True)
                    
        return df


class FeatureEngineer:
    """Create and transform features"""
    
    @staticmethod
    def create_price_features(price_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create price-based features for churn analysis
        
        Args:
            price_df: Price DataFrame with columns: id, price_date, price_p*_var, price_p*_fix
            
        Returns:
            DataFrame with engineered price features
        """
        try:
            # Convert to datetime
            price_df = price_df.copy()
            price_df['price_date'] = pd.to_datetime(price_df['price_date'], format='%Y-%m-%d')
            
            # Calculate mean prices for different time periods
            mean_year = price_df.groupby('id').mean().reset_index()
            mean_6m = price_df[price_df['price_date'] > '2015-06-01'].groupby('id').mean().reset_index()
            mean_3m = price_df[price_df['price_date'] > '2015-10-01'].groupby('id').mean().reset_index()
            
            # Rename columns for clarity
            period_configs = [
                (mean_year, 'mean_year'),
                (mean_6m, 'mean_6m'),
                (mean_3m, 'mean_3m')
            ]
            
            for df, prefix in period_configs:
                rename_dict = {
                    'price_p1_var': f'{prefix}_price_p1_var',
                    'price_p2_var': f'{prefix}_price_p2_var',
                    'price_p3_var': f'{prefix}_price_p3_var',
                    'price_p1_fix': f'{prefix}_price_p1_fix',
                    'price_p2_fix': f'{prefix}_price_p2_fix',
                    'price_p3_fix': f'{prefix}_price_p3_fix'
                }
                df.rename(columns=rename_dict, inplace=True)
                
                # Create combined price features
                df[f'{prefix}_price_p1'] = df[f'{prefix}_price_p1_var'] + df[f'{prefix}_price_p1_fix']
                df[f'{prefix}_price_p2'] = df[f'{prefix}_price_p2_var'] + df[f'{prefix}_price_p2_fix']
                df[f'{prefix}_price_p3'] = df[f'{prefix}_price_p3_var'] + df[f'{prefix}_price_p3_fix']
            
            # Merge all features
            features = pd.merge(mean_year, mean_6m, on='id', how='inner')
            features = pd.merge(features, mean_3m, on='id', how='inner')
            
            # Remove redundant columns (price_date)
            cols_to_drop = [col for col in features.columns if col.startswith('price_') and '_' not in col.split('_', 1)[1]]
            features.drop(columns=cols_to_drop, inplace=True, errors='ignore')
            
            logger.info(f"Created price features with shape {features.shape}")
            return features
            
        except Exception as e:
            logger.error(f"Error creating price features: {str(e)}")
            raise


# Convenience functions
def load_and_validate(filepath: str) -> pd.DataFrame:
    """Load a file and validate its integrity"""
    df = DataLoader.load_data(filepath)
    validator = DataValidator()
    
    missing = validator.check_missing_values(df)
    if missing['critical_columns']:
        logger.warning(f"Columns with >50% missing values: {missing['critical_columns']}")
    
    duplicates, pct = validator.check_duplicates(df)
    if pct > 0:
        logger.warning(f"Found {duplicates} duplicate rows ({pct:.2f}%)")
    
    return df
