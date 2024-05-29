import pandas as pd
from .pandas_tools import replace_text

def currency_clean(df: pd.DataFrame, col: str, currency_sufix: str = "Â\xa0MXN", k_sep: str = ".",
                   decimal_sep: str = ",", use_cents: bool = False) -> pd.Series:
    """Cleans the DataFrame column that stores currency data (MXN)
    and transforms it into int values."""

    safe_df = df.copy()
    safe_df[col] = replace_text(safe_df, col, currency_sufix)
    # Wix manage the thounsand separator as "."
    # so removing it will help to make it an integet value
    safe_df[col] = replace_text(safe_df, col, k_sep)

    safe_df[col] = replace_text(safe_df, col, decimal_sep, ".")

    if use_cents:
        # Remember that any language has trouble to stored float values
        # making a standar to stored float data as integer and consider
        # it when managing the data.

        # Because the clients doesn't use cents, this is setted as False,
        # but keep it in mind for the furure if it's required.

        # Before this step, the value stored in the column was a STRING
        # Not any numeric value
        safe_df[col] = safe_df[col].astype(float)
        safe_df[col] = safe_df[col] * 100
    else:
        # If it doesn't use cents, then you must delete them according to
        # the logic above and because it will cause an error next
        safe_df[col] = replace_text(safe_df, col, ".00")
    
    return safe_df[col].astype(int)