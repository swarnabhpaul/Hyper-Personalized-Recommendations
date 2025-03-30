import tensorflow as tf
from tensorflow.keras.models import load_model
from database import get_customer_by_cid, get_last_n_loan_applications_by_cid, get_df_from_table
import joblib
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

def readable_loan_name(loan_type):
    return " ".join([word.capitalize() for word in loan_type.split('_')]) + " Loan"

def recommend_loan(cid:int, n_recommendations:int=6):
    """Generates loan recommendations for a customer based on their loan application history.
    """
    model = load_model('initial_data/loan_approval_model.keras')
    preprocessor = joblib.load('initial_data/preprocessor_loan.joblib')

    customer = get_customer_by_cid(cid, as_df=True).iloc[0]
    if customer.empty:
        raise ValueError("Customer not found")

    customer_loans = get_last_n_loan_applications_by_cid(cid, n=10, as_df=True)
    debt_to_income = 0.5
    credit_score = 650
    annual_income = customer['annual_income']

    if not customer_loans.empty:
        debt_to_income = customer_loans['debt_to_income_ratio'].mean()
        credit_score = customer_loans['credit_score'].mean()

    original_loan_products = get_df_from_table('loan_products', index_col='loan_product_id')
    loan_products = get_df_from_table('loan_products')

    ids = loan_products['loan_product_id']
    loan_products.drop(columns=['loan_product_id'], inplace=True)

    loan_products['annual_income_x'] = annual_income
    loan_products['annual_income_y'] = annual_income
    loan_products['debt_to_income_ratio'] = debt_to_income
    loan_products['credit_score'] = credit_score
    loan_products['loan_amount'] = (loan_products['min_loan_amount'] + loan_products['max_loan_amount']) / 2
    loan_products['interest_rate'] = (loan_products['min_interest_rate'] + loan_products['max_interest_rate']) / 2
    loan_products['loan_term_months'] = (loan_products['min_term_months'] + loan_products['max_term_months']) / 2

    date = pd.to_datetime('today')
    month = date.month
    app_month_sin = np.sin(2 * np.pi * month / 12)
    app_month_cos = np.cos(2 * np.pi * month / 12)
    loan_products['app_month_sin'] = app_month_sin
    loan_products['app_month_cos'] = app_month_cos

    customer_attributes = ['age', 'gender', 'education']
    loan_products[customer_attributes] = customer[customer_attributes]

    column_order = [
        'loan_amount', 'interest_rate', 'loan_term_months', 'credit_score', 'annual_income_x',
        'debt_to_income_ratio', 'age', 'gender', 'annual_income_y', 'education', 'loan_type',
        'purchase_category', 'min_interest_rate', 'max_interest_rate', 'min_term_months',
        'max_term_months', 'min_loan_amount', 'max_loan_amount', 'processing_fee',
        'app_month_sin', 'app_month_cos'
    ]

    loan_products = loan_products.reindex(columns=column_order)

    print(loan_products.iloc[0])
    
    # print(loan_products.columns)
    X = preprocessor.transform(loan_products)
    # print(X)
    y_pred = model.predict(X)
    loan_products['approval_probability'] = y_pred
    loan_products['loan_product_id'] = ids
    loan_products = loan_products.sort_values('approval_probability', ascending=False)

    recommended_loans = loan_products[['loan_product_id', 'approval_probability']].head(n_recommendations)

    keep_cols_loan = ['loan_type', 'purchase_category', 'min_interest_rate', 'max_interest_rate', 'min_term_months', 'max_term_months', 'min_loan_amount', 'max_loan_amount', 'processing_fee']
    recommended_loans[keep_cols_loan] = original_loan_products[keep_cols_loan].loc[recommended_loans['loan_product_id']].values
    
    recommended_loans['loan_type_readable'] = recommended_loans['loan_type'].apply(readable_loan_name)

    return recommended_loans.head(n_recommendations)


if(__name__ == '__main__'):
    print(recommend_loan(1))