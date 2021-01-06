from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

class Features_engineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        
        ### A line of code is needed here 
        just_to_add_a_line = 42

    def fit(self, X, y=None):

        return self

    def transform(self, X, y=None):

        X = X.copy()
        
        
        imputer = SimpleImputer(strategy='most_frequent')

        X.loc[:,'product_category_name_english'] = imputer.fit_transform(
            X)

        family = ['bed_bath_table', 'furniture_decor', 'garden_tools', 'home_appliances',
                  'home_construction', 'home_confort', 'furniture_living_room',
                  'kitchen_dining_laundry_garden_furniture',
                  'home_appliances_2', 'costruction_tools_garden',
                  'furniture_bedroom',
                  'small_appliances_home_oven_and_coffee',
                  'furniture_mattress_and_upholstery', 'home_comfort_2',
                  'la_cuisine', 'fixed_telephony', 'toys',
                  'cool_stuff', 'baby', 'fashion_childrens_clothes',
                  'christmas_supplies', 'air_conditioning',
                  'housewares', 'pet_shop', 'small_appliances',
                  'diapers_and_hygiene', 'party_supplies',
                  'cine_photo', 'dvds_blu_ray', 'tablets_printing_image',
                  'sports_leisure',
                  'watches_gifts', 'flowers', 'auto',
                  'food', 'drinks', 'food_drink', 'agro_industry_and_commerce']

        business = ['security_and_services',
                    'construction_tools_safety', 'construction_tools_construction', 'costruction_tools_tools',
                    'signaling_and_security', 'construction_tools_lights',
                    'industry_commerce_and_business',
                    'market_place',
                    'office_furniture',
                    'stationery']

        electronics_sport = ['computers_accessories', 'telephony', 'electronics',
                             'consoles_games', 'audio',
                             'computers', 'fashion_male_clothing']

        fashion_beauty = ['fashion_bags_accessories', 'luggage_accessories', 'fashion_shoes',
                          'fashion_underwear_beach',
                          'fashio_female_clothing', 'fashion_sport', 'health_beauty', 'perfumery']

        culture = ['books_technical', 'arts_and_craftmanship', 'books_imported', 'books_general_interest',
                   'music', 'cds_dvds_musicals', 'art', 'musical_instruments']

        list_of_categories = [family, business,
                      electronics_sport, fashion_beauty, culture]
        
        conditions = [X['product_category_name_english'].isin(
            category) for category in list_of_categories]
        
        choices = ['family', 'business',
                   'electronics_sport', 'fashion_beauty', 'culture']

        X.loc[:,'prod_category'] = np.select(
            conditions, choices, default=np.nan)

        X = X.drop('product_category_name_english', axis=1)

        return X



class log_transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        
        ### A line of code is needed here 
        just_to_add_a_line = 42

    def fit(self, X, y=None):

        return self

    def transform(self, X, y=None):

        X = X.copy()
        
        num_data = X.select_dtypes(['int64', 'float64'])
    
        num_data = np.log(num_data + 1)
    
        cat_data = X.select_dtypes('object')
    
        X = pd.concat([num_data,cat_data], axis = 1)
        
        return X
        


