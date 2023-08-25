import pandas as pd

datos = {
    "Nombres": ["Maria","Luis","Carmen"],
    "Materias": ["Matematicas","Programacion","Mercadotecnia"],
    "Promedio": [80,90,100]
}

df_alumnos = pd.DataFrame(datos)
print(df_alumnos)

#dataframe
df_colesterol= pd.read_csv("https://raw.githubusercontent.com/asalber/"
                          "manual-python/master/datos/colesteroles.csv", sep=";",decimal=",")
#print(df_colesterol)

#print(df_colesterol.sample(5))

#print(df_colesterol.info())
#print(df_colesterol.shape)
#print(df_colesterol.size)
#print(df_colesterol.columns)
#print(df_colesterol.dtypes)
#print(df_colesterol.index)

print(df_colesterol[["nombre","edad","colesterol"]])
