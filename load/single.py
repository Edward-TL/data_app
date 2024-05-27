import pandas as pd
from openpyxl import load_workbook

def df_to_excel(
        df, path, file_name,
        sheet_name:str = "Hoja 1", style = None) -> None:
    """"""
    if file_name.endswith(".xlsx") == False:
         file_name += '.xlsx'

    excel_file = f'{path}\\{file_name}'

    with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='a') as writer:
        # Tables Schema
        df.to_excel(writer, sheet_name = sheet_name, index = False)

        worksheet = writer.sheets[sheet_name]
