import pandas as pd

data_frame = pd.read_csv("dataset/db.csv")

user_id = {}
product_id = {}

for count, id in enumerate(data_frame["user_id"]):
    if not id in user_id:
        user_id[id] = len(user_id)

for id in data_frame["product_id"]:
    if not id in product_id:
        product_id[id] = len(product_id)

print(len(product_id))
print(len(user_id))

matrix = [[0]*len(product_id) for i in range(len(user_id))]


for index, row in data_frame.iterrows():
    matrix[user_id[row.iloc[0]]][product_id[row.iloc[1]]] = row.iloc[2]
  
data_frame = pd.DataFrame(matrix)
data_frame.to_csv("dataset/matrix.csv")
