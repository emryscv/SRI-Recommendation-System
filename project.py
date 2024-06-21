import pandas as pd

from utils import ratings_matrix_creator
from utils import items_variances
from utils import pearson_similarity
from utils import predict_rating_with_variance_adjustment
from utils import get_top_k_neighbors 

data = {'user': ['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Bob', 'Bob', 'Carol', 'Carol', 'Carol', 'Carol', 'Carol', 'Dave', 'Dave', 'Dave', 'Dave', 'Dave'],
        'item': ['Item1', 'Item2', 'Item3', 'Item4', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5'],
        'rating': [5, 3, 4, 4, 3, 1, 2, 3, 3, 4, 3, 4, 3, 5, 3, 3, 1, 5, 4]}

ratings_df = pd.DataFrame(data)

ratings_matrix = ratings_matrix_creator(ratings_df)

items_variancess = items_variances(ratings_matrix)

similarity_matrix = pearson_similarity(ratings_matrix, items_variancess)

predict_rating = predict_rating_with_variance_adjustment('Alice','Item5', 2 , similarity_matrix, ratings_matrix)

print(predict_rating)
