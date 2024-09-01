import pandas as pd
import math
import numpy as np


def mean_adj_matrix_load():

    ret = matrix.copy().astype(float)
    

    for index, row in ret.iterrows() :
        mean = row.replace(0, np.nan).mean()
        for col in ret.columns:
            if(matrix.loc[index,col]!=0):
             ret.loc[index,col] = ret.loc[index,col]-mean
        
    return ret

def sim(a,b):

    num = 0
    left = 0
    right = 0

    for index, row in mean_adj_matrix.iterrows():
        if(matrix.loc[index,a]!=0 and matrix.loc[index,b]!=0 ):
            left += math.pow(row[a],2)
            right += math.pow(row[b],2)
            num += row[a]*row[b]

    if (left == 0 or right == 0):
        return 0 
    
    return num/(math.sqrt(left)*math.sqrt(right))

def sim_matrix(matrix):

    similarity_matrix = pd.DataFrame(columns=matrix.columns, index=matrix.columns,dtype=float)

    for row in similarity_matrix.index:
        for col in similarity_matrix.columns:
            if(row == col):
                similarity_matrix.loc[row,col] = 1
            else:
                value = sim(row,col)
                similarity_matrix.loc[row,col] = value
                similarity_matrix.loc[col,row] = value

    return similarity_matrix


matrix = pd.read_json('dataset/Ratings.json')
mean_adj_matrix = mean_adj_matrix_load()

simi_matrix = sim_matrix(matrix)

simi_matrix.to_json('dataset/IB_sim_matrix')

