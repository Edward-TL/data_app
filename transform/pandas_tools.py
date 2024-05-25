import pandas as pd

def replace_text(df, col, or_text, new_text="") -> pd.Series:
    """Replace the string stored on the column cells. If the new_text is not given, it will
    just delete it from the string"""

    return df[col].str.replace(or_text, new_text)

def replace_many_texts(df, col, conditions: dict[str: str]) -> pd.Series:
    """Replace the string stored on the column cells. If the new_text is not given, it will
    just delete it from the string"""

    df_col = df[col]
    for or_text, new_text in conditions.items():
        df_col = df_col.str.replace(or_text, new_text)

    return df