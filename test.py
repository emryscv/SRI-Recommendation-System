import pandas as pd
import dealer
import item_based_recomendation as ibr
import basic_recomendation as br
import time
import numpy as np
import statistics

# data = [
#         [5,3,4,4,0],
#         [3,1,2,3,3],
#         [4,3,4,3,5],
#         [3,3,1,5,4],
#         [1,5,5,2,1]
# ]
# column=['Item1','Item2','Item3','Item4','Item5']
# rows=['Alice','Bob','Carol','Dave','Paul']

# data2 = [
#         [0,3,0,4,5],
#         [5,3,0,0,0],
#         [0,5,4,3,0],
#         [0,0,0,3,4],
#         [5,0,4,0,3]
# ]

# column2=['Item1','Item2','Item3','Item4','Item5']
# rows2=['User1','User2','User3','User4','User5']

# ratings_matrix = pd.DataFrame(data, columns=column, index=rows)

##### TEST #####

dealer.load_dataset()

inicio = time.time()
x = dealer.get_potential_predictions(1)
final = time.time()

print(x)

print(f"done in {final-inicio}")


##### OTHER TEST #####

# df = pd.read_json('dataset/Ratings.json')


# ibr.load_matrix(df)

# x = ibr.get_sim_matrix()

# y = (x.loc[2])

# row = ibr.get_mean_adj_matrix()

# row = (row.loc[1])

# rowm = df.loc[1]

# num = 0
# den = 0



# for i in range(1,1001):
    
#     if((row[i]>0) and (i != 14)):
#         num = num + (y[i]*row[i])
#         den = den + y[i]

# media = rowm.replace(0, np.nan).mean()


# print(media+(num/den))

# print()




