import pandas as pd
import dealer
import item_based_recomendation as ibr
import basic_recomendation as br
import time

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

df = pd.read_json('dataset/Ratings.json')

inicio = time.time()
ibr.load_matrix(df)
final = time.time()

print(f"done in {final-inicio}")

