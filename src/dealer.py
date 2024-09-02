import pandas as pd
import basic_recommendation as br
import item_based_recommendation as ibr
import knowledge_based_recommendation as kbr
import random

dataset = None 
products = None
loaded = False
items_amount = 5
neigbours_amount = 5
item_based=True


def load_dataset():
    """
    Carga el conjunto de datos desde los archivos JSON y los almacena en las variables globales 'dataset' y 'products'.
    
    """
    
    global dataset
    global loaded
    global products
    dataset = pd.read_json('src/dataset/Ratings.json')
    products = pd.read_json('src/dataset/Products.json')
    loaded = True
    
def get_items():
    if(not loaded):
        load_dataset()
    
    x=[]

    for i in products.index:
        x.append(products.loc[i])

    return x


def get_categories():
    """
    Retorna un diccionario con las categorías de los productos cargados en el dataset.
    Retorna:
        dict: Un diccionario donde las claves son los nombres de las columnas del dataset
              (excepto 'Price') y los valores son listas de valores únicos en cada columna.
    """
    
    if(not loaded):
        load_dataset()
    
    x = {}

    for column in products.columns:
        if(column != 'Price'):
            x[column] = list(products[column].drop_duplicates())

    return x

def get_max_price():
    """
    Obtiene el precio máximo de los productos.
    Retorna:
        precio maximo
    """

    return max(products["Price"])
    
def get_load_state():
    """
    Obtiene el estado de carga.
    Retorna:
        bool: El estado de carga.
    """

    return loaded

def change_items_amount(value):
    """
    Cambia la cantidad de elementos.
    Parámetros:
    - value: El nuevo valor de la cantidad de elementos.
    """
    
    items_amount
    items_amount = value

def change_neigbours_amount(value):
    """
    Cambia la cantidad de vecinos para el sistema de recomendación.
    Parámetros:
    - value: int, la nueva cantidad de vecinos a considerar.
    """

    global neigbours_amount
    neigbours_amount = value

def change_coll_methof():
    """
    Cambia el método de recomendación utilizado por el sistema.
    Esta función cambia el valor de la variable global 'item_based' a su valor opuesto.
    Si 'item_based' es True, se cambiará a False, y viceversa.

    """

    global item_based
    item_based = not item_based

def get_recomendations(filters:dict, items:dict):
    """
    Obtiene las recomendaciones basadas en los filtros proporcionados y los elementos disponibles.
    Parámetros:
        filters (dict): Un diccionario que contiene los filtros a aplicar. Las claves son los nombres de los filtros y los valores son los valores de los filtros.
        items (dict): Un diccionario que contiene los elementos disponibles. Las claves son los identificadores de los elementos y los valores son los datos de los elementos.
    Retorna:
        dic: Un diccionario de recomendaciones basadas en los filtros aplicados.
    """

    aux = {}
    for key, value in items.items():
        i = int(key.split(",")[0])
        aux[i] = value

    items = aux

    
    for key, value in filters.items():
        if(key == 'Price'):
            kbr.set_price_lower_filter(value)
        else:
            kbr.set_eq_filter(value,key)

    filtered_products = list((kbr.apply_filter()).index)

    recomendation = compute_predictions(items, filtered_products)

    return recomendation


##### Método del Grafo #####

def get_liked_items(user):
    """
    Obtiene los elementos que le gustan al usuario.
    Parámetros:
        user (dict): Un diccionario que representa las preferencias del usuario, donde las claves son los elementos y los valores son las calificaciones.
    Retorna:
        list: Una lista de elementos que le gustan al usuario, es decir, aquellos elementos que tienen una calificación igual o mayor a 3.
    """
    
    liked_items = []

    matrix = user

    for key, value in matrix.items():
        if  value>= 3:
            liked_items.append(key)
    
    return liked_items

def get_related_users(liked_items):
    """
    Obtiene una lista de usuarios relacionados basados en los elementos que les gustaron.
    Parámetros:
        liked_items (list): Una lista de elementos que les gustaron a los usuarios.
    Retorna:
        list: Una lista de usuarios relacionados.
    """
    
    global dataset
    related_users = []

    for item in liked_items:
        col = dataset[item] 
        for index, value in col.items():
            if index not in related_users and value>=3:
                related_users.append(index)
    
    return related_users

def get_posible_items(user):
    """
    Obtiene una lista de posibles elementos recomendados para un usuario dado.
    Parámetros:
        user (dic): Diccionario de los elementos que calificó el ususario
    Retorna:
        list: Una lista de elementos posibles recomendados para el usuario dado.
    """
 

    global dataset
    liked_items = get_liked_items(user)
    related_users = get_related_users(liked_items)
    
    posible_items=[]

    for users in related_users:
        row = dataset.loc[users].items()
        for index, value in row:
            if(index not in user and index not in posible_items and value>=3):
                posible_items.append(index)
    return posible_items

def compute_predictions(user, filtered_items):
    """
    Calcula las predicciones de recomendación para un usuario dado y una lista de elementos filtrados.
    Parámetros:
    - user: Un diccionario que representa al usuario.
    - filtered_items: Una lista de elementos filtrados.
    Retorna:
    Un diccionario ordenado de elementos posibles y sus respectivas puntuaciones de predicción.
    """

    global dataset
    global items_amount
    global neigbours_amount
    global item_based
    posible_items = []
    work_items = []
    aux_items = []

    pred = None

    if(item_based):
        ibr.load_matrix(dataset)
        pred = ibr.pred2
    else:
        br.load_matrix(dataset)
        pred = br.predict_rating


    if(len(filtered_items)>items_amount):
        posible_items = get_posible_items(user)
        while(len(filtered_items)>0 and len(work_items)!=items_amount):
            aux = random.choice(filtered_items)
            filtered_items.remove(aux)
            if(aux in posible_items):
                work_items.append(aux)
            else:
                aux_items.append(aux)
        if(len(filtered_items)==0):
            while(work_items!=items_amount):
                aux = random.choice(aux_items)
                aux_items.remove(aux)
                work_items.append(aux)
        filtered_items = work_items

    if(len(filtered_items)==0):
        filtered_items = random.sample(get_posible_items(user),items_amount)


    posible_items_rating = {}

    for item in filtered_items:
        if item not in user:
            posible_items_rating[item] = pred(user, item)

    print(posible_items_rating)

    return dict(sorted(posible_items_rating.items(), key=lambda item: item[1], reverse=True))



