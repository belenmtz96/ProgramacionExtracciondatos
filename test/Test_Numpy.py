import numpy as np

l = [[1,2,3,4,5] , [6,7,8,9,10]]
n1 = np.array(l)
print(n1)
#verificar dato
print(type(n1))

#Principales atributos
print(n1.ndim) #Numero de dimensiones
print(n1.shape) #Regresarte a una tupla, dimensiones
print(n1.size) #cantidad de elementos
print(n1.dtype) #Tipo de dato

#Acceso a los elementos
print(n1[1, 2]) # Primer nuemro es el renglon, segundo numero es la columna
print(n1 *2) #Multiplicar las columnas

print(np.linalg.norm(n1))

print(n1.transpose())
print(n1.mean()) #promedio de los datos

#Promedio por una columna
print(n1[0, :].mean())


ecuaciones = [[1,2],[3,5]]

np_ecuaciones = np.array(ecuaciones)
resultados = np.array([1,2])
print(np.linalg.solve(np_ecuaciones,resultados))