import pandas as pd

dados = {
    "nome": ["Ana", "Carlos", "Marina"],
    "curso": ["ADS","Engenharia", "ADS"],
    "nota": [8.5, 7.0, 9.2]
}

df = pd.DataFrame(dados)

print (df)