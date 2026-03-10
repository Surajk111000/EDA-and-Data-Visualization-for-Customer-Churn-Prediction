"""
Visualization functions for EDA and analysis
"""
import logging
from typing import Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

# Set plotting style
sns.set(color_codes=True)
sns.set_style("whitegrid")


class ChartConfig:
    """Configuration for charts"""
    DEFAULT_FIGSIZE = (12, 6)
    LARGE_FIGSIZE = (18, 10)
    EXTRA_LARGE_FIGSIZE = (18, 25)
    TITLE_FONTSIZE = 14
    LABEL_FONTSIZE = 12
    COLOR_PALETTE = sns.color_palette("husl", 8)


class Visualizer:
    """Create professional visualizations"""
    
    @staticmethod
    def plot_stacked_bars(dataframe: pd.DataFrame, title: str, 
                         figsize: Tuple[int, int] = ChartConfig.DEFAULT_FIGSIZE,
                         rotation: int = 0, legend_loc: str = "upper right") -> None:
        """
        Plot stacked bar chart with annotations
        
        Args:
            dataframe: DataFrame with data to plot
            title: Chart title
            figsize: Figure size (width, height)
            rotation: X-axis label rotation
            legend_loc: Legend location
        """
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            dataframe.plot(
                kind="bar",
                stacked=True,
                ax=ax,
                rot=rotation,
                color=ChartConfig.COLOR_PALETTE[:len(dataframe.columns)]
            )
            
            ax.set_title(title, fontsize=ChartConfig.TITLE_FONTSIZE, fontweight='bold')
            ax.set_ylabel("Company base (%)", fontsize=ChartConfig.LABEL_FONTSIZE)
            
            # Annotate bars
            Visualizer._annotate_stacked_bars(ax, textsize=11)
            
            # Update legend
            if len(dataframe.columns) == 2:
                ax.legend(["Retention", "Churn"], loc=legend_loc)
            else:
                ax.legend(loc=legend_loc)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting stacked bars: {str(e)}")
            raise
    
    @staticmethod
    def _annotate_stacked_bars(ax, pad: float = 0.99, colour: str = "white", 
                              textsize: int = 13) -> None:
        """
        Add value annotations to stacked bars
        
        Args:
            ax: Matplotlib axis
            pad: Padding for annotation placement
            colour: Text color
            textsize: Text size
        """
        for patch in ax.patches:
            value = round(patch.get_height(), 1)
            if value == 0.0:
                continue
            
            x_pos = (patch.get_x() + patch.get_width() / 2) * pad - 0.05
            y_pos = (patch.get_y() + patch.get_height() / 2) * pad
            
            ax.annotate(
                str(value),
                (x_pos, y_pos),
                color=colour,
                size=textsize,
                ha='center',
                fontweight='bold'
            )
    
    @staticmethod
    def plot_distribution(dataframe: pd.DataFrame, column: str, 
                         figsize: Tuple[int, int] = ChartConfig.DEFAULT_FIGSIZE,
                         bins: int = 50) -> None:
        """
        Plot distribution histogram for a column
        
        Args:
            dataframe: DataFrame with 'churn' column
            column: Column to plot
            figsize: Figure size
            bins: Number of bins
        """
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            temp_data = pd.DataFrame({
                "Retention": dataframe[dataframe["churn"] == 0][column],
                "Churn": dataframe[dataframe["churn"] == 1][column]
            })
            
            temp_data[["Retention", "Churn"]].plot(
                kind='hist',
                bins=bins,
                ax=ax,
                stacked=True,
                color=['#2ecc71', '#e74c3c']
            )
            
            ax.set_xlabel(column, fontsize=ChartConfig.LABEL_FONTSIZE)
            ax.set_ylabel("Frequency", fontsize=ChartConfig.LABEL_FONTSIZE)
            ax.set_title(f"Distribution of {column}", fontsize=ChartConfig.TITLE_FONTSIZE, 
                        fontweight='bold')
            ax.ticklabel_format(style='plain', axis='x')
            ax.legend(["Retention", "Churn"])
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting distribution: {str(e)}")
            raise
    
    @staticmethod
    def plot_boxplots(dataframe: pd.DataFrame, columns: list, 
                     figsize: Tuple[int, int] = ChartConfig.LARGE_FIGSIZE) -> None:
        """
        Create multiple boxplots for outlier detection
        
        Args:
            dataframe: DataFrame
            columns: List of columns to plot
            figsize: Figure size
        """
        try:
            n_plots = len(columns)
            fig, axs = plt.subplots(nrows=n_plots, figsize=figsize)
            
            if n_plots == 1:
                axs = [axs]
            
            for idx, col in enumerate(columns):
                sns.boxplot(data=dataframe, y=col, ax=axs[idx], color='skyblue')
                axs[idx].set_title(f"Boxplot: {col}", fontsize=ChartConfig.TITLE_FONTSIZE, 
                                  fontweight='bold')
                axs[idx].ticklabel_format(style='plain', axis='y')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting boxplots: {str(e)}")
            raise
    
    @staticmethod
    def plot_correlation_matrix(dataframe: pd.DataFrame, 
                               figsize: Tuple[int, int] = (14, 12)) -> None:
        """
        Plot correlation heatmap
        
        Args:
            dataframe: DataFrame with numeric columns
            figsize: Figure size
        """
        try:
            fig, ax = plt.subplots(figsize=figsize)
            
            corr_matrix = dataframe.corr()
            
            mask = None
            sns.heatmap(
                corr_matrix,
                mask=mask,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
                ax=ax,
                annot_kws={'size': 9}
            )
            
            ax.set_title("Correlation Matrix", fontsize=ChartConfig.TITLE_FONTSIZE, 
                        fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting correlation matrix: {str(e)}")
            raise
    
    @staticmethod
    def plot_churn_analysis(client_df: pd.DataFrame) -> None:
        """
        Plot overall churn statistics
        
        Args:
            client_df: Client DataFrame
        """
        try:
            churn = client_df[['id', 'churn']].copy()
            churn.columns = ['Companies', 'churn']
            
            churn_counts = churn.groupby('churn').size()
            churn_pct = (churn_counts / churn_counts.sum()) * 100
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=ChartConfig.DEFAULT_FIGSIZE)
            
            # Count plot
            colors = ['#2ecc71', '#e74c3c']
            ax1.bar(['No Churn', 'Churn'], churn_counts.values, color=colors)
            ax1.set_title('Churn Count', fontsize=ChartConfig.TITLE_FONTSIZE, fontweight='bold')
            ax1.set_ylabel('Number of Companies')
            
            # Pie chart
            ax2.pie(churn_pct, labels=['No Churn', 'Churn'], autopct='%1.1f%%',
                   colors=colors, startangle=90)
            ax2.set_title('Churn Percentage', fontsize=ChartConfig.TITLE_FONTSIZE, fontweight='bold')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting churn analysis: {str(e)}")
            raise
    
    @staticmethod
    def plot_categorical_churn(dataframe: pd.DataFrame, column: str,
                              figsize: Tuple[int, int] = ChartConfig.LARGE_FIGSIZE) -> None:
        """
        Plot churn rate by categorical variable
        
        Args:
            dataframe: DataFrame with 'id', column, and 'churn'
            column: Categorical column to analyze
            figsize: Figure size
        """
        try:
            grouped = dataframe[['id', column, 'churn']].copy()
            churn_by_cat = grouped.groupby([column, 'churn'])['id'].count().unstack(fill_value=0)
            churn_pct = churn_by_cat.div(churn_by_cat.sum(axis=1), axis=0) * 100
            churn_pct = churn_pct.sort_values(by=1, ascending=False) if 1 in churn_pct.columns else churn_pct
            
            fig = Visualizer.plot_stacked_bars(churn_pct, f'Churn by {column}', 
                                             figsize=figsize, rotation=45)
            return fig
            
        except Exception as e:
            logger.error(f"Error plotting categorical churn: {str(e)}")
            raise


class QuickPlots:
    """Quick plotting functions for exploratory analysis"""
    
    @staticmethod
    def summary_statistics(dataframe: pd.DataFrame) -> None:
        """Print summary statistics"""
        print(dataframe.describe())
    
    @staticmethod
    def data_info(dataframe: pd.DataFrame) -> None:
        """Print data information"""
        dataframe.info()
    
    @staticmethod
    def missing_values_plot(dataframe: pd.DataFrame) -> None:
        """Plot missing values percentage"""
        missing = (dataframe.isnull().sum() / len(dataframe)) * 100
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if len(missing) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            missing.plot(kind='barh', ax=ax, color='coral')
            ax.set_xlabel('Missing Percentage (%)')
            ax.set_title('Missing Values by Column')
            plt.tight_layout()
            return fig
        else:
            print("No missing values found")
