import pandas as pd

df = pd.read_csv(
    "alunos_800.csv",
    sep=";",
    decimal=",",
    encoding="utf-8",
)

print (df)