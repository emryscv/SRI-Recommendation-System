import pandas as pd
import numpy as np
import math
import statistics

matrix = None
mean_adj_matrix = None
similarity_matrix = None

def get_sim_matrix():
    return similarity_matrix

def get_mean_adj_matrix():
    return mean_adj_matrix

def load_matrix(data):
    global matrix 
    global similarity_matrix

    matrix = data
    mean_adj_matrix_load()
    similarity_matrix = pd.read_json('src/dataset/IB_sim_matrix.json')

def mean_adj_matrix_load():
    global mean_adj_matrix

    ret = matrix.copy().astype(float)

    for index, row in ret.iterrows():
        mean = row.replace(0, np.nan).mean()
        for col in ret.columns:
            if matrix.loc[index, col] != 0:
                ret.loc[index, col] = ret.loc[index, col] - mean

    mean_adj_matrix = ret

def sim(a, b):
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

def pred(u,p):
   
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

    mean = statistics.mean(list(u.values()))
    row = u.copy()
    for key, value in row.items():
        value = value - mean
    sim = similarity_matrix.loc[p]
    
    num = 0
    den = 0

    for key, value in row.items():
        if key != p and value > 0:
         num = num + (sim[key]*value)
         den = den + sim[key]


    return mean+(num/den)