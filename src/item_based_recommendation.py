import pandas as pd
import numpy as np
import math
import statistics

matrix = None
mean_adj_matrix = None
similarity_matrix = None

def get_sim_matrix():
    """
    Obtiene la matriz de similitud.
    Retorna:
        similarity_matrix: La matriz de similitud.
    """
    
    return similarity_matrix

def get_mean_adj_matrix():
    """
    Obtiene la matriz de adyacencia media.
    Retorna: mean_adj_matrix.
    """
    
    return mean_adj_matrix

def load_matrix(data):
    """
    Carga una matriz de datos y asigna los valores a las variables globales 'matrix' y 'similarity_matrix'.
    Parámetros:
    - data: La matriz de datos a cargar.
    """
    
    global matrix 
    global similarity_matrix

    matrix = data
    mean_adj_matrix_load()
    similarity_matrix = pd.read_json('src/dataset/IB_sim_matrix.json')

def mean_adj_matrix_load():
    """
    Carga la matriz de ajuste de media.
    Esta función calcula y carga la matriz de ajuste de media, que es una versión modificada de la matriz original. 
    La matriz de ajuste de media se obtiene restando la media de cada fila a los elementos no nulos de esa fila.
   
    """

    global mean_adj_matrix

    ret = matrix.copy().astype(float)

    for index, row in ret.iterrows():
        mean = row.replace(0, np.nan).mean()
        for col in ret.columns:
            if matrix.loc[index, col] != 0:
                ret.loc[index, col] = ret.loc[index, col] - mean

    mean_adj_matrix = ret

def sim(a, b):
    """
    Calcula la similitud entre dos elementos a y b utilizando el método de recomendación basado en ítems.
    Parámetros:
    - a: El primer elemento a comparar.
    - b: El segundo elemento a comparar.
    Retorna:
    - El valor de similitud entre los elementos a y b.
    """
    
    num = 0
    left = 0
    right = 0

    for index, row in mean_adj_matrix.iterrows():
        if matrix.loc[index, a] != 0 and matrix.loc[index, b] != 0:
            left += math.pow(row[a], 2)
            right += math.pow(row[b], 2)
            num += row[a] * row[b]

    if left == 0 or right == 0:
        return 0

    return num / (math.sqrt(left) * math.sqrt(right))

def sim_matrix():
    """
    Calcula y devuelve una matriz de similitud basada en los datos de entrada.
    Retorna:
        similarity_matrix (pandas.DataFrame): Una matriz de similitud donde las filas y columnas representan los elementos
        de los datos de entrada y los valores representan la similitud entre los elementos.
    """

    global similarity_matrix
    similarity_matrix = pd.DataFrame(
        columns=matrix.columns, index=matrix.columns, dtype=float
    )

    for row in similarity_matrix.index:
        for col in similarity_matrix.columns:
            if row == col:
                similarity_matrix.loc[row, col] = 1
            else:
                value = sim(row, col)
                similarity_matrix.loc[row, col] = value
                similarity_matrix.loc[col, row] = value

def top_k_items(item, k):
    return similarity_matrix.loc[item].drop(item).nlargest(k).index

def pred(u, p):

    """
    Calcula la predicción de valor para un usuario y un ítem específico.
    Parámetros:
    - u (int): El ID del usuario.
    - p (str): El ID del ítem.
    Retorna:
    - float: El valor de la predicción.
    """
    
    row = mean_adj_matrix.loc[u]
    sim = similarity_matrix.loc[p]
    rowm = matrix.loc[u]
    
    num = 0
    den = 0
    for item in matrix.columns:
        if item != p and row[item] > 0:
         num = num + (sim[item]*row[item])
         den = den + sim[item]

    med = rowm.replace(0, np.nan).mean()

    return med+(num/den)

def pred2(u:dict,p):
    def pred2(u: dict, p) -> float:
        """
        Calcula la predicción de un usuario para un ítem específico utilizando el enfoque basado en ítems.
        Parámetros:
        - u (dict): Diccionario que representa las calificaciones de un usuario para diferentes ítems.
        - p: Ítem específico para el cual se desea calcular la predicción.
        Retorna:
        - float: Valor de la predicción para el usuario y el ítem dado.
        """

    mean = statistics.mean(list(u.values()))
    row = u.copy()
    for key, value in row.items():
        row[key] = value - mean
    sim = similarity_matrix.loc[p]
    
    num = 0
    den = 0

    for key, value in row.items():
        if key != p and value > 0:
         num = num + (sim[key]*u[key])
         den = den + sim[key]


    return mean+(num/den)