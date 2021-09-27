from typing import List
import pandas as pd
import os

filefolder: str = r'\\home.gu.gu.se\home-XB$\xbrjos\Documents\EPA Database Assignment\Data Uni GU'
xlsname: str = 'BLEPA 5.xlsx'

filepath: str = os.path.join(filefolder, xlsname)
data: pd.DataFrame = pd.read_excel(filepath, sheet_name=None)
sheets: List[str] = list(data.keys())
print(f'{len(sheets)} Sheets')
sheet1 = data[sheets[0]]
