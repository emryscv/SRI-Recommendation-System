import pandas as pd

df = pd.read_json('src/dataset/Products.json')


filters = {
    'Product Name': None,
    'Brand': None,
    'Category': None,
    'Price': None,
    'Color': None,
    'Size': None
}

def set_eq_filter(list,property):
    """
    Establece un filtro de igualdad para una lista de valores en una propiedad específica.

    Parámetros:
        list (list): La lista de valores a filtrar.
        property (str): La propiedad en la que se aplicará el filtro.

    """
    global filters
    if(list != None and len(list)>0):
        filter_cond = (df[property] == list[0])
        if(len(list)>1):
            for x in range(1,len(list)):
                filter_cond = filter_cond | (df[property] == list[x])
        filters[property] = filter_cond

def set_price_range_filter(low,high):
    """
    Establece un filtro de rango de precios para el sistema de recomendación.
    Parámetros:
    low (float): El valor mínimo del rango de precios.
    high (float): El valor máximo del rango de precios.
    """

    global filters
    filters['Price'] = (df['Price']<=high) & (df['Price']>=low)

def set_price_lower_filter(price):
    """
    Establece un filtro para el precio inferior en el sistema de recomendación.
    Parámetros:
    - price: int
        El precio máximo permitido para los productos recomendados.
    """

    global filters
    if(price != None):
        filters['Price'] = df['Price']<=price

def apply_filter():
    """
    Aplica los filtros especificados al dataframe y devuelve el dataframe filtrado.
    Returns:
        pandas.DataFrame: El dataframe filtrado.
    """

    dff = df.copy()

    for key, values in filters.items():
        if(values is not None):
            if(key=='Price'):
                dff = dff[values]
            else:
                dff = dff[values]

    return dff

    
