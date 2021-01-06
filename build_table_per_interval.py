import pandas as pd
import numpy as np
from category_encoders import OneHotEncoder
from sklearn.impute import SimpleImputer




### Function that filters the orders by date interval and merges the tables into a single table
def aggregate_per_time_interval(date_interval):
    
    ### Importing
    customer_data = pd.read_csv('Data/olist_customers_dataset.csv' )
    geolocation_data = pd.read_csv('Data/olist_geolocation_dataset.csv')
    order_items_data = pd.read_csv('Data/olist_order_items_dataset.csv')
    order_payments_data= pd.read_csv('Data/olist_order_payments_dataset.csv')
    order_reviews_data = pd.read_csv('Data/olist_order_reviews_dataset.csv')
    olist_order_data = pd.read_csv('Data/olist_orders_dataset.csv')
    olist_products_data = pd.read_csv('Data/olist_products_dataset.csv')
    olist_sellers_data = pd.read_csv('Data/olist_sellers_dataset.csv')
    olist_product_category_data = pd.read_csv('Data/product_category_name_translation.csv')
    
    
    ### Converts column of interest to datetime format
    
    olist_order_data['order_purchase_timestamp'] = pd.to_datetime(olist_order_data['order_purchase_timestamp']) 
    
    ### Keeps dates that are between the given date limits
    
    mask = (olist_order_data['order_purchase_timestamp'] >= date_interval[0]) & (olist_order_data
                                        ['order_purchase_timestamp'] < date_interval[1])
    olist_order_data = olist_order_data[mask]
    
    ### Rest of function is the same as in first notebook of the project
    
    
    
    
    
    
    ### Olist_products_dataset merge to get product category name in english
    olist_products_data = olist_products_data.merge(olist_product_category_data, 
                                how = 'left', on = 'product_category_name')
    
    ### Merge order items dataset with products dataset
    order_items_data = order_items_data.merge(olist_products_data, how = 'left', 
                                on = 'product_id')
    
    
    
    
    ### Count number of occurrences for each order ID
    count = order_items_data.groupby('order_id').count().iloc[:,0].rename('n_items per order')
    
    ### Numeric data will be aggregated by mean
    num_order_items_data = pd.concat([order_items_data['order_id'], 
            order_items_data.select_dtypes('float64')], axis = 1)
    
    num_order_items_data = num_order_items_data.groupby('order_id').mean()
    
    
    ### Aggregate each order's products category names by its most frequent value
    cat_order_items_data = order_items_data[['order_id', 
            'product_category_name_english']].groupby('order_id').agg(lambda g : 
                    g.value_counts().index[0] if np.any(g.notnull()) else np.nan)
    
    order_items_data = pd.concat([count, num_order_items_data, cat_order_items_data], axis = 1)
    
    
    olist_order_data = olist_order_data.merge(order_items_data, how = 'left', 
                                on = 'order_id')
    
    
    
    
    ### Number of payments
    ###1. Count the number 
    
    ### Count number of payments per order
    
    
    count = order_payments_data.groupby('order_id').count().iloc[:,0].rename('n_payments per order')
    
    
    

    ### One hot encode payment type feature
    
    enc = OneHotEncoder(cols = ['payment_type'],use_cat_names=True)
    order_payments_data = enc.fit_transform(order_payments_data)
    
    order_payments_data = order_payments_data.drop('payment_type_not_defined', axis = 1)
                                                                                    
    
    order_payments_data = order_payments_data.groupby('order_id').mean()
    
    
    order_payments_data = pd.concat([order_payments_data, count], axis = 1)
    
    olist_order_data = olist_order_data.merge(order_payments_data, how = 'left',
                                on = 'order_id')
    
    
    
    ### Number of reviews per order
    
    count = order_reviews_data.groupby('order_id').count().iloc[:,0].rename(
        'n_reviews per order').astype('float64')
    
    order_reviews_data = order_reviews_data[['order_id', 'review_score']].groupby('order_id').mean()
    
    order_reviews_data = pd.concat([count, order_reviews_data], axis = 1)
    
    olist_order_data = olist_order_data.merge(order_reviews_data, how = 'left', 
                                    on = 'order_id')
    
        
    ### Merging customer table with order tables
    
    customer_data = customer_data.merge(olist_order_data, how = 'inner', 
                            on = 'customer_id')
    
    ### Cutomer data aggregation
    count = customer_data.groupby('customer_unique_id').count().iloc[:,0].rename('n_orders per customer')
    

    ### Numeric features aggregated by mean
    numeric_customer_data = pd.concat([customer_data.select_dtypes('float64'),customer_data[
        'customer_unique_id']], axis = 1)
    
    numeric_customer_data = numeric_customer_data.groupby('customer_unique_id').mean()
    
    ### Categorical features aggregated by most frequent value
    cat_customer_data = customer_data[['customer_unique_id', 'product_category_name_english']].groupby(
    'customer_unique_id').agg(lambda g : 
                    g.value_counts().index[0] if np.any(g.notnull()) else np.nan)
    
    
    customer_data = pd.concat([count, numeric_customer_data, cat_customer_data], axis = 1)
    
    return customer_data

