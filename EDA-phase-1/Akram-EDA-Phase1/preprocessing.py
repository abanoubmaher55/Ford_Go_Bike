"""Data Preprocessing and Exploration Module.

Provides utility functions for inspecting data completeness, generating summary
statistics, handling missing values, and engineering baseline features.

Note:
    This module contains dataset-specific logic tailored for bike-share data:
    - Expects 'member_birth_year' for demographic and age calculations.
    - Uses custom imputation logic for 'member_gender' and station metadata.
"""

import pandas as pd


def read_files(file_path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file.

    Args:
        file_path (str): The filesystem path or URL to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    return pd.read_csv(file_path)


def check_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize data types and unique value counts for all columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Table containing 'Dtype' and 'Num_Unique' per column.
    """
    dtypes = df.dtypes
    n_unique = df.nunique()
    return pd.DataFrame({"Dtype": dtypes, "Num_Unique": n_unique})


def get_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate transposed descriptive statistics for numeric columns rounded to two decimals.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Summary statistics (mean, std, min, quartiles, max) for numeric columns.
    """
    return df.describe().T.round(2)


def get_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptive statistics including the Interquartile Range (IQR).

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transposed descriptive statistics with an added 'IQR' column.
    """
    stats = df.describe().T
    stats["IQR"] = stats["75%"] - stats["25%"]
    return stats.round(2)


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """Generate non-null counts, null counts, null percentages, and data types for each column.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Summary table containing column-level completeness metrics.
    """
    return pd.DataFrame(
        {
            "Non-Null Count": df.notnull().sum(),
            "Null Count": df.isnull().sum(),
            "Null %": (df.isnull().sum() / len(df) * 100).round(2),
            "Dtype": df.dtypes,
        }
    )


def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Identify and rank columns that contain missing values.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Subset of columns with missing data, sorted descending by missing count.
    """
    null_counts = df.isnull().sum()
    missing = null_counts[null_counts > 0]
    return (
        pd.DataFrame(
            {
                "Missing Count": missing,
                "Missing %": (missing / len(df) * 100).round(2),
            }
        )
        .sort_values(by="Missing Count", ascending=False)
    )


def get_missing_rows(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Retrieve the first n rows that contain at least one null value.

    Args:
        df (pd.DataFrame): Input DataFrame.
        n (int, optional): Number of rows to return. Defaults to 5.

    Returns:
        pd.DataFrame: First n rows containing missing values.
    """
    return df[df.isnull().any(axis=1)].head(n)


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values based on column type and naming convention.

    Imputation strategy:
    - Numeric features containing 'year': imputed using column median.
    - Other numeric and non-numeric columns: imputed using column mode.
    - Excludes 'member_gender' to allow explicit custom handling.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Copy of DataFrame with specified missing values imputed.
    """
    df = df.copy()
    cols_with_nulls = [
        col
        for col in df.columns
        if df[col].isnull().any() and col != "member_gender"
    ]

    for col in cols_with_nulls:
        if df[col].dtype in ["int64", "float64"]:
            fill_val = df[col].median() if "year" in col else df[col].mode()[0]
            df[col] = df[col].fillna(fill_val)
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    return df


def fill_gender_na(
    df: pd.DataFrame, fill_value: str = "Unknown"
) -> pd.DataFrame:
    """Impute missing values in the 'member_gender' column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        fill_value (str, optional): Fallback category to use. Defaults to "Unknown".

    Returns:
        pd.DataFrame: Copy of DataFrame with 'member_gender' nulls filled.
    """
    df = df.copy()
    df["member_gender"] = df["member_gender"].fillna(fill_value)
    return df


def check_duplicates(df: pd.DataFrame) -> int:
    """Count the total number of duplicate rows.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        int: Total count of duplicate rows.
    """
    return df.duplicated().sum()


def inspect_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics for all object and categorical columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Categorical summary including count, unique, top, and frequency.
    """
    return df.select_dtypes(include="object").describe()


def convert_to_category(
    df: pd.DataFrame, columns: list = None
) -> pd.DataFrame:
    """Convert a target list of columns to pandas 'category' dtype.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list, optional): List of column names to convert. Defaults to None.

    Returns:
        pd.DataFrame: Copy of DataFrame with converted categorical columns.
    """
    df = df.copy()
    if columns:
        for col in columns:
            df[col] = df[col].astype("category")
    return df


def calculate_age(df: pd.DataFrame, reference_year: int) -> pd.DataFrame:
    """Calculate member age using birth year and an anchor reference year.

    Args:
        df (pd.DataFrame): Input DataFrame containing 'member_birth_year'.
        reference_year (int): The baseline year used to compute age (e.g., dataset collection year).

    Returns:
        pd.DataFrame: Copy of DataFrame with a new 'age' column.
    """
    df = df.copy()
    df["age"] = reference_year - df["member_birth_year"]
    return df


def convert_to_int(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Cast a specific column to integer dtype.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the column to cast.

    Returns:
        pd.DataFrame: Copy of DataFrame with the column cast to int.
    """
    df = df.copy()
    df[column] = df[column].astype(int)
    return df


def average_col(df: pd.DataFrame, column: str) -> float:
    """Compute the arithmetic mean of a designated numeric column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the numeric column to average.

    Returns:
        float: Mean value of the column.
    """
    return df[column].mean()