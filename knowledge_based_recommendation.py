import pandas as pd

df = pd.read_json('dataset/Products.json')


filters = {
    'Product Name': None,
    'Brand': None,
    'Category': None,
    'Price': None,
    'Color': None,
    'Size': None
}

def set_eq_filter(list,property):
    global filters
    if(list != None):
        filter_cond = (df[property] == list[0])
        if(len(list)>1):
            for x in range(1,len(list)):
                filter_cond = filter_cond | (df[property] == list[x])
        filters[property] = filter_cond

def set_price_range_filter(low,high):
    global filters
    filters['Price'] = (df['Price']<=high) & (df['Price']>=low)

def set_price_lower_filter(price):
    global filters
    if(price != None):
        filters['Price'] = df['Price']<=price

def apply_filter():

    dff = df.copy()

    for key, values in filters.items():
        if(values is not None):
            if(key=='Price'):
                dff = dff[values]
            else:
                dff = dff[values]

    return dff

    
