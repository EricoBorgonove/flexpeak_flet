import pandas as pd

df = pd.read_excel(
    "alunos_800.xlsx",
    sheet_name="Alunos",
)

print(df)