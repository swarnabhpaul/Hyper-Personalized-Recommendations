from database import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import logging

def product_similarity():
    """Computes the cosine similarity between products based on their features. 
    Can be run on product updates to get the updated similarity matrix.
    
    Keyword arguments:
    Return: cosine similarity matrix between products
    """
    
    products = get_df_from_table('products')
    businesses = get_df_from_table('businesses')

    # merge products and businesses
    products = products.merge(businesses, on='bid', how='left')
    #oneHotEncode the categories
    products = pd.get_dummies(products, columns=['category'])

    # Standardize numerical columns
    numerical_cols = ['popularity', 'price', 'revenue', 'num_employees']
    products[numerical_cols] = StandardScaler().fit_transform(products[numerical_cols])

    cosine_sim = cosine_similarity(products.drop(['bid', 'pid', 'product_name', 'business_name', 'geo_demand'], axis=1))

    # convert to DataFrame
    product_similarity_df = pd.DataFrame(cosine_sim, index=products.pid, columns=products.pid)
    return product_similarity_df

def customer_similarity(n_transactions:int=None):
    """Computes the cosine similarity between customers based on their purchase history and profile.
    Can be run on demand with n_transactions, or on a schedule to update the similarity matrix.
    
    Keyword arguments:
    n_transactions -- Number of TOTAL transactions to consider (default: entire history)
    Return: cosine similarity matrix between customers based on last n_transactions transactions in the database
    """
    
    # get the data and one hot encode the categorical columns
    customers = get_df_from_table('customers', index_col='cid')
    customers = pd.get_dummies(customers, columns=['gender', 'education'])

    transactions = get_df_from_table('transactions', limit=n_transactions, order_by='purchase_date', order='desc')
    products = get_df_from_table('products')
    businesses = get_df_from_table('businesses')
    
    # merge transactions with products and businesses
    products = products.merge(businesses[['bid', 'category']], on='bid', how='left')
    products.drop('bid', axis=1, inplace=True)
    keep_cols_product = ['pid', 'popularity', 'price', 'category']
    transactions = transactions.merge(products[keep_cols_product], on='pid', how='left')

    # pivot table to get the amount spent by each customer in each category
    sim_matrix = transactions.pivot_table(index='cid', columns=['category'], values='amount', fill_value=0)

    categorical_features_customers = ['name', 'location', 'occupation']
    sim_matrix = sim_matrix.reindex(index=customers.index, fill_value=0)
    sim_matrix = pd.merge(sim_matrix, customers.drop(columns=categorical_features_customers), on='cid', how='left')

    # Standardize numerical columns
    numerical_cols = ['Clothing', 'Dining', 'Education', 'Electronics', 'Entertainment',
       'Groceries', 'Health', 'Travel', 'age', 'annual_income']
    sim_matrix[numerical_cols] = StandardScaler().fit_transform(sim_matrix[numerical_cols])

    # Compute cosine similarity between customers
    user_similarity = cosine_similarity(sim_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=sim_matrix.index, columns=sim_matrix.index)
    return user_similarity_df

def sentiment_scores(n:int=None):
    """Gets the average sentiment score of each category based on the last n posts in the database.
    
    Keyword arguments:
    n -- Number of posts to consider
    Return: a DataFrame with the average sentiment score of each category
    """
    
    avg_recent_sentiment = get_avg_recent_sentiment(n, as_df=True)
    return avg_recent_sentiment

def get_product_recommendations(cid:int, n_transactions:int=10, n_transactions_customer:int=10000, n_customers:int=5, n_similar_products:int=5, n_posts:int=1000, n_recommendations:int=5, product_weight:float=0.5, customer_weight:float=0.5, sentiment_weight:float=0.3, repeat_prob:float=0.3):
    """Generates product recommendations for a customer based on their purchase history, similar customers, and category sentiment scores.
    
    Keyword arguments:
    cid -- id of the customer
    n_transactions -- number of recent transactions for each customer to consider (default: 10)
    n_transactions_customer -- number of total transactions to consider for computing customer similarity (default: 10000)
    n_customers -- number of similar customers to consider (default: 5)
    n_similar_products -- number of similar products to consider (default: 5)
    n_posts -- number of recent posts to consider for sentiment analysis (default: 1000)
    n_recommendations -- number of recommendations to generate (default: 5)
    product_weight -- weight for product similarity (default: 0.5)
    customer_weight -- weight for customer similarity (default: 0.5)
    sentiment_weight -- weight for category sentiment scores (default: 0.3)
    repeat_prob -- probability of keeping repeat purchases (default: 0.3)

    Return: return_description
    """
    
    products_df = get_df_from_table('products')
    businesses_df = get_df_from_table('businesses')
    products_df = products_df.merge(businesses_df[['bid', 'category']], on='bid', how='left')
    products_df.set_index('pid', inplace=True)
    
    recent_transactions = get_last_n_transactions_for_customer(cid, n=n_transactions, as_df=True)
    unique_pids = recent_transactions["pid"].unique()

    products_df['score'] = 0.0

    # increase score for similar products
    product_similarity_df = product_similarity()
    for pid in unique_pids:
        similar_products = product_similarity_df[pid].sort_values(ascending=False)[1:1+n_similar_products].index
        for similar_pid in similar_products:
            score = product_similarity_df[pid][similar_pid]
            products_df.loc[similar_pid, 'score'] += score * product_weight
    
    last_n = get_last_n_transactions_for_all_customers(n=n_transactions, as_df=True)

    # increase score for products bought by similar customers in the same amount of transactions
    user_similarity_df = customer_similarity(n_transactions=n_transactions_customer)
    similar_customers = user_similarity_df[cid].sort_values(ascending=False)[1:1+n_customers].index
    for similar_cid in similar_customers:
        similar_transactions = last_n[similar_cid]
        for pid in similar_transactions['pid'].unique():
            score = product_similarity_df[pid][similar_pid]
            products_df.loc[pid, 'score'] += score * customer_weight

    # increase score for products belonging to categories with high sentiment scores
    sentiment_scores_df = sentiment_scores(n=n_posts)
    for category, row in sentiment_scores_df.iterrows():
        products_df.loc[products_df['category'] == category, 'score'] += row['avg_sentiment'] * sentiment_weight

    # randomly decrease score for repeat products with probability 1 - repeat_prob
    for pid in unique_pids:
        if np.random.rand() > repeat_prob:
            products_df.loc[pid, 'score'] *= 0.2 # penalise repeat purchases

    # get top n recommendations
    recommendations = products_df.sort_values(by='score', ascending=False)[:n_recommendations]
    recommendations['pid'] = recommendations.index
    recommendations = recommendations.merge(businesses_df[['bid', 'business_name']], on='bid', how='left')
    return recommendations

if __name__ == '__main__':
    cid = int(input("Enter the customer id: "))
    recommendations = get_product_recommendations(cid)
    print(recommendations)
    close_connection()


