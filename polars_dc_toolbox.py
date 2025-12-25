"""
Polars Data Science Toolbox
===========================

A collection of utility extensions for Polars DataFrames designed to enhance 
exploratory data analysis (EDA) and cleaning workflows. 

This module uses monkey patching to extend the `pl.DataFrame` namespace directly.

Author:  Mauricio Zárate Romero (ZarRomM)
Contact: mauriciozarom@gmail.com
Profile: https://github.com/ZarRomM
License: CC BY-NC 4.0 (Non-Commercial Use Only)
Version: 1.0.0
"""

import polars as pl
import sys

def _pandas_style_info(self) -> None:
    """
    Prints a concise summary of the DataFrame, mimicking pandas.DataFrame.info().

    It displays the index dtype, column dtypes, non-null values, and memory usage.
    Useful for a quick overview of the dataset structure.

    Returns:
        None: This method prints to stdout and returns nothing.
    """
    n_rows, n_cols = self.shape
    print(f"<class 'polars.DataFrame'>")
    print(f"RangeIndex: {n_rows} entries, 0 to {n_rows - 1}")
    print(f"Data columns (total {n_cols} columns):")
    
    # Header formatting with fixed width
    print(f"{'#':<4} {'Column':<25} {'Non-Null Count':<15} {'Dtype':<10}")
    print("-" * 60)
    
    try:
        # Efficiently calculate nulls for all columns at once
        null_counts = self.null_count().row(0)
        
        for idx, (col_name, dtype) in enumerate(self.schema.items()):
            non_null = n_rows - null_counts[idx]
            print(f"{idx:<4} {col_name:<25} {non_null:<15} {str(dtype):<10}")
            
        print("-" * 60)
        
        # Memory usage estimation
        mem_usage = self.estimated_size()
        if mem_usage > 1024**2:
            mem_str = f"{mem_usage / (1024**2):.2f} MB"
        else:
            mem_str = f"{mem_usage / 1024:.2f} KB"
            
        unique_dtypes = set(str(t) for t in self.dtypes)
        print(f"dtypes: {', '.join(unique_dtypes)}")
        print(f"memory usage: {mem_str}")
        
    except Exception as e:
        print(f"Error generating info report: {e}", file=sys.stderr)


def _null_report(self) -> None:
    """
    Generates and prints a detailed report of missing values in the DataFrame.

    Calculates the absolute count and percentage of nulls per column,
    sorting the results by missing data percentage in descending order.

    Returns:
        None: Prints a table or a success message if no nulls are found.
    """
    total_rows = self.height
    
    # Calculate nulls, transpose to vertical format, and add percentage
    try:
        null_stats = (
            self.null_count()
            .transpose(include_header=True, header_name="column_name")
            .rename({"column_0": "null_count"})
            .with_columns(
                (pl.col("null_count") / total_rows * 100).round(2).alias("null_percentage")
            )
            .filter(pl.col("null_count") > 0)
            .sort("null_percentage", descending=True)
        )

        print(f"--- Missing Values Report (Total Rows: {total_rows}) ---")
        
        if null_stats.is_empty():
            print("✅ No missing values found in the dataset.")
        else:
            print(null_stats)
            
    except Exception as e:
        print(f"Error generating null report: {e}", file=sys.stderr)


def _clean_column_names(self) -> pl.DataFrame:
    """
    Standardizes column names to 'snake_case'.

    Converts all column names to lowercase and replaces spaces with underscores.
    This creates a new DataFrame and does not modify the original one in-place
    (Polars is immutable).

    Returns:
        pl.DataFrame: A new DataFrame with sanitized column names.
        
    Example:
        >>> df = df.clean_names()
    """
    return self.select(
        pl.all().name.to_lowercase().name.map(lambda x: x.replace(" ", "_"))
    )


# --- REGISTRATION LOGIC ---

def register_extensions():
    """
    Registers the custom methods to the polars.DataFrame class.
    
    This function checks if the methods already exist to prevent 
    accidental overwrites of native Polars functionality in the future.
    """
    extensions = [
        ("info", _pandas_style_info),
        ("null_report", _null_report),
        ("clean_names", _clean_column_names)
    ]
    
    registered_count = 0
    for name, func in extensions:
        if not hasattr(pl.DataFrame, name):
            setattr(pl.DataFrame, name, func)
            registered_count += 1
            
    if registered_count > 0:
        print(f"✅ Polars Toolbox: {registered_count} extensions registered successfully.")

# Execute registration on import
if __name__ != "__main__":
    register_extensions()