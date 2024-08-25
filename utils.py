
import pandas as pd
import basic_recomendation as br
import item_based_recomendation as ibr

global dataset
global loaded 
loaded = False

def load_dataset():
    global dataset
    global loaded
    dataset = pd.read_csv('dataset/matrix.csv')
    loaded = True
    
def get_items():
    try:
       x = dataset.columns
    except :
        return []
    return list(dataset.columns)

def get_load_state():
    return loaded


##### Método del Grafo #####

def get_liked_items(user, rating_matrix):

    liked_items = []

    matrix = rating_matrix.loc[user]

    for item in matrix.index:
        if  matrix[item]>= 3:
            liked_items.append(item)
    return liked_items

def get_related_users(liked_items, rating_matrix, user):

    related_users = []

    for item in liked_items:
        matrix = rating_matrix[item].index  
        for users in matrix:
            if users not in related_users and users!=user:
                related_users.append(users)
    return related_users

def get_posible_items(user,rating_matrix,amount):

    liked_items = get_liked_items(user,rating_matrix)
    related_users = get_related_users(liked_items,rating_matrix,user)
    
    posible_items=[]

    for users in related_users:
        row = rating_matrix.loc[users].index
        for item in row:
            #if item not in liked_items and item not in posible_items and amount != 0:
            if rating_matrix.loc[user][item] == 0 and item not in posible_items and amount != 0:
                posible_items.append(item)
                amount = amount-1
    return posible_items

def get_potential_predictions(user, neigbours_amount, items_amount, rating_matrix, item_based=True):

    pred = None

    if(item_based):
        ibr.load_matrix(rating_matrix)
        pred = ibr.pred
    else:
        br.load_matrix(rating_matrix)
        pred = br.predict_rating

    posible_items = get_posible_items(user, rating_matrix, items_amount)

    posible_items_rating = {}

    for item in posible_items:
        posible_items_rating[item] = pred(user, item, neigbours_amount)

    return posible_items_rating



        