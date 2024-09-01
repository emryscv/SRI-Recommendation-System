import pandas as pd
import basic_recomendation as br
import item_based_recomendation as ibr

dataset = None 
products = None
loaded = False
items_amount = 10
neigbours_amount = 10
item_based=True

def load_dataset():
    global dataset
    global loaded
    global products
    dataset = pd.read_json('dataset/Ratings.json')
    products = pd.read_json('dataset/Products.json')
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

##### Método del Grafo #####

def get_liked_items(user):
    global dataset
    liked_items = []

    matrix = dataset.loc[user]

    for item in matrix.index:
        if  matrix[item]>= 3:
            liked_items.append(item)
    return liked_items

def get_related_users(liked_items, user):
    global dataset
    related_users = []

    for item in liked_items:
        matrix = dataset[item].index  
        for users in matrix:
            if users not in related_users and users!=user:
                related_users.append(users)
    return related_users

def get_posible_items(user,amount):
    global dataset
    liked_items = get_liked_items(user)
    related_users = get_related_users(liked_items,user)
    
    posible_items=[]

    for users in related_users:
        row = dataset.loc[users].index
        for item in row:
            #if item not in liked_items and item not in posible_items and amount != 0:
            if dataset.loc[user][item] == 0 and item not in posible_items and amount != 0:
                posible_items.append(item)
                amount = amount-1
    return posible_items

def get_potential_predictions(user):

    global dataset
    global items_amount
    global neigbours_amount
    global item_based

    pred = None

    if(item_based):
        ibr.load_matrix(dataset)
        pred = ibr.pred
    else:
        br.load_matrix(dataset)
        pred = br.predict_rating

    posible_items = get_posible_items(user, items_amount)

    posible_items_rating = {}

    for item in posible_items:
        posible_items_rating[item] = pred(user, item, neigbours_amount)

    return posible_items_rating

def get_recommendation(filter, ratings):
    print(filter)
    print(ratings)
    return {}        