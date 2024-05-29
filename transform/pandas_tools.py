import pandas as pd

def replace_text(df, col, or_text, new_text="") -> pd.Series:
    """Replace the string stored on the column cells. If the new_text is not given, it will
    just delete it from the string"""

    return df[col].str.replace(or_text, new_text)

def replace_many_texts(df, col, conditions: dict[str: str]) -> pd.Series:
    """Replace the string stored on the column cells. If the new_text is not given, it will
    just delete it from the string"""

    for or_text, new_text in conditions.items():
        df[col] = df[col].str.replace(or_text, new_text)

    return df

def range_filter(df, col:str, start = '2024-01-01', end = '2024-02-01') -> pd.DataFrame:
    """Sugar sintax for a df filter based on range. Setted for date values, but can be
    used for numeric values"""
    return df.loc[
            (df[col] >= start)
            & (df[col] < end)
        ]

def digit_filter(digit: int):
    """Simple filter for doble digit strings when is required"""
    if digit <= 9:
        return f'0{digit}'
    
    return str(digit)

def month_filter(df, col, month, year: int = 2024, day: int = 1):
    """Makes a query between dates in the dataframe column passed.
    Remember that the date structure is needed as YYYY-MM-DD. Any
    change on this will return an error by pandas, not the function."""

    # Due to the add operation, the use of digit_filter func makes it
    # take more time
    if month < 9:
        str_month = f'0{month}'
        end_month = f'0{month + 1}'
    
    elif month == 9:
        str_month = f'09'
        end_month = f'10'
    
    else:
        # 10 - 11. If 
        str_month = str(month)
        end_month = str(month + 1)    


    start_date = f"{year}-{str_month}-{digit_filter(day)}"
    end_date = f"{year}-{end_month}-{digit_filter(day)}"
    
    return range_filter(df, col, start_date, end_date)

def nested_group_by(df, by_cols) -> pd.DataFrame:
    """
    This tool is created for an interaction bucle. With this,
    yo can pass de df and columns to grupo and it will store in
    a callabe way the dataframe.
    """
    return df.groupby(
            by = by_cols
        ).sum()

def sells_pivot(
        df, values: str = "Ventas brutas",
        index: str = "Nombre del Item",
        columns: str = "Canal de ventas",
        total_col: bool = False, total_row: bool = False,
        nan_filler = 0) -> pd.DataFrame:
    """Creates a pivot table with the data passed, but takes out the extra
    row created on the header due to Multi-index. Also, replace all NaN values
    with 0. If another value is needed, pass it through the nan_filler.
    
    If Total row or column are required, set the values to True and it will append it."""
    
    pivot = pd.DataFrame(
            df.pivot_table(
            values = values,
            index= index,
            columns= columns
        ).fillna(
            nan_filler
            # Creates a array of arrays, witch the Dataframe
            # constructor will take and create a regular df
            ).to_records()
    )

    if total_row:
        pivot.loc['Total'] = pivot.sum(numeric_only=True, axis = 0)
        pivot[pivot.columns[0]].fillna("Total", inplace=True)
        
    if total_col:
        pivot['Total'] = pivot.sum(numeric_only=True, axis = 1)

    return pivot