import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

import loan_recommendation
from loan_recommendation import readable_loan_name, recommend_loan

class TestLoanRecommendation(unittest.TestCase):

    def test_readable_loan_name(self):
        # Test the helper that converts "personal_loan" to "Personal Loan Loan"
        result = readable_loan_name("personal_loan")
        # "personal_loan" becomes ["Personal", "Loan"] then joined to "Personal Loan", then " Loan" appended.
        self.assertEqual(result, "Personal Loan Loan")
    
    @patch('loan_recommendation.get_df_from_table')
    @patch('loan_recommendation.get_last_n_loan_applications_by_cid')
    @patch('loan_recommendation.get_customer_by_cid')
    @patch('loan_recommendation.joblib.load')
    @patch('loan_recommendation.load_model')
    def test_recommend_loan(self, mock_load_model, mock_joblib_load, 
                            mock_get_customer_by_cid, mock_get_last_n_loans, 
                            mock_get_df_from_table):
        # --- Set up fake model and preprocessor ---
        fake_model = MagicMock()
        # Fake predict returns an array with one prediction: 0.8 probability.
        fake_model.predict.return_value = np.array([[0.8]])
        mock_load_model.return_value = fake_model

        fake_preprocessor = MagicMock()
        # We need to return an array of shape (n_samples, num_features). The column order has 21 columns.
        fake_preprocessor.transform.return_value = np.array([[0.5]*21])
        mock_joblib_load.return_value = fake_preprocessor

        # --- Set up fake customer data ---
        # Return a DataFrame with one customer row.
        customer_df = pd.DataFrame([{
            'cid': 1,
            'annual_income': 60000,
            'age': 35,
            'gender': 'm',
            'education': 'b'
        }])
        # get_customer_by_cid is called with as_df=True; we need to return a DataFrame with a row.
        mock_get_customer_by_cid.return_value = customer_df

        # --- Set up fake loan application data ---
        # Return a DataFrame with loan application history.
        loans_df = pd.DataFrame([
            {'debt_to_income_ratio': 0.4, 'credit_score': 700},
            {'debt_to_income_ratio': 0.5, 'credit_score': 750}
        ])
        mock_get_last_n_loans.return_value = loans_df

        # --- Set up fake loan products data ---
        # original_loan_products: first call to get_df_from_table with index_col.
        original_loan_products = pd.DataFrame([{
            'loan_product_id': 101,
            'loan_type': 'personal_loan',
            'purchase_category': 'electronics',
            'min_interest_rate': 5.0,
            'max_interest_rate': 10.0,
            'min_term_months': 12,
            'max_term_months': 60,
            'min_loan_amount': 1000,
            'max_loan_amount': 5000,
            'processing_fee': 2.0
        }]).set_index('loan_product_id')
        # loan_products: second call returns similar data but with loan_product_id as a column.
        loan_products = pd.DataFrame([{
            'loan_product_id': 101,
            'loan_type': 'personal_loan',
            'purchase_category': 'electronics',
            'min_interest_rate': 5.0,
            'max_interest_rate': 10.0,
            'min_term_months': 12,
            'max_term_months': 60,
            'min_loan_amount': 1000,
            'max_loan_amount': 5000,
            'processing_fee': 2.0
        }])
        # When recommend_loan calls get_df_from_table twice for 'loan_products',
        # return the original_loan_products on first call and loan_products on second call.
        mock_get_df_from_table.side_effect = [original_loan_products, loan_products]

        # --- Call recommend_loan ---
        # Use n_recommendations=1 to keep it simple.
        recommended = recommend_loan(1, n_recommendations=1)

        # --- Verify outputs ---
        # Check that the recommendation DataFrame has one row.
        self.assertEqual(len(recommended), 1)
        # Check that the loan_product_id is 101.
        self.assertEqual(recommended.iloc[0]['loan_product_id'], 101)
        # Verify that the approval_probability column is added and equals 0.8.
        self.assertAlmostEqual(recommended.iloc[0]['approval_probability'], 0.8)
        # Verify that the loan_type_readable column is computed correctly.
        self.assertEqual(recommended.iloc[0]['loan_type_readable'], "Personal Loan Loan")
    
    def test_recommend_loan_customer_not_found(self):
        # To simulate a "customer not found" scenario without triggering an IndexError,
        # we return a DataFrame with one row that is an empty Series.
        empty_series = pd.Series({}, dtype=object)
        # Note: The DataFrame itself is not empty (has one row), but the row (Series) is empty.
        df = pd.DataFrame([empty_series])
        with patch('loan_recommendation.get_customer_by_cid') as mock_get_customer:
            mock_get_customer.return_value = df
            with self.assertRaises(ValueError) as context:
                recommend_loan(999)
            self.assertIn("Customer not found", str(context.exception))

if __name__ == '__main__':
    unittest.main()
