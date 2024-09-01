import pandas as pd
import basic_recomendation as br
import item_based_recomendation as ibr
import knowledge_based_recommendation as kbr
import random

dataset = None 
products = None
loaded = False
items_amount = 5
neigbours_amount = 5
item_based=True


def load_dataset():
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
    if(not loaded):
        load_dataset()
    
    x = {}

    for column in products.columns:
        if(column != 'Price'):
            x[column] = list(products[column].drop_duplicates())

    return x

def get_max_price():
    return max(products["Price"])
    
def get_load_state():
    return loaded

def change_items_amount(value):
    items_amount
    items_amount = value

def change_neigbours_amount(value):
    global neigbours_amount
    neigbours_amount = value

def change_coll_methof():
    global item_based
    item_based = not item_based

def get_recomendations(filters:dict, items:dict):

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

    liked_items = []

    matrix = user

    for key, value in matrix.items():
        if  value>= 3:
            liked_items.append(key)
    
    return liked_items

def get_related_users(liked_items):
    global dataset
    related_users = []

    for item in liked_items:
        col = dataset[item] 
        for index, value in col.items():
            if index not in related_users and value>=3:
                related_users.append(index)
    
    return related_users

def get_posible_items(user):

    global dataset
    liked_items = get_liked_items(user)
    related_users = get_related_users(liked_items)
    
    posible_items=[]

    for users in related_users:
        row = dataset.loc[users].items()
        for index, value in row:
            #if item not in liked_items and item not in posible_items and amount != 0:
            #if dataset.loc[user][item] == 0 and item not in posible_items and amount != 0:
            if(index not in user and index not in posible_items and value>=3):
                posible_items.append(index)
    return posible_items

def compute_predictions(user, filtered_items):

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

    return dict(sorted(posible_items_rating.items(), key=lambda item: item[1], reverse=True))



