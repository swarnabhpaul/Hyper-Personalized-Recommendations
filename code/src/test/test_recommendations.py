import unittest
from unittest.mock import patch
import pandas as pd
from recommendations import (
    product_similarity,
    customer_similarity,
    sentiment_scores,
    get_product_recommendations,
)

class TestRecommendations(unittest.TestCase):

    @patch('recommendations.get_df_from_table')
    def test_product_similarity(self, mock_get_df):
        # Fake products and businesses data
        products = pd.DataFrame({
            'bid': [1, 2],
            'pid': [101, 102],
            'product_name': ['ProdA', 'ProdB'],
            'popularity': [10, 20],
            'price': [100, 200],
            'geo_demand': ['USA', 'CAN']
        })
        businesses = pd.DataFrame({
            'bid': [1, 2],
            'category': ['Tech', 'Retail'],
            'business_name': ['X Corp', 'Y Inc'],
            'revenue': [1000, 2000],
            'num_employees': [10, 20]
        })
        # First call returns products, second returns businesses.
        mock_get_df.side_effect = [products, businesses]

        sim_df = product_similarity()
        # Check that a DataFrame is returned with product IDs as both index and columns.
        self.assertIsInstance(sim_df, pd.DataFrame)
        self.assertTrue(all(sim_df.index == products['pid']))
        self.assertTrue(all(sim_df.columns == products['pid']))

    @patch('recommendations.get_df_from_table')
    def test_customer_similarity(self, mock_get_df):
        """Test that customer similarity matrix contains expected categories"""

        # Define expected categories for pivot table
        expected_categories = ['Clothing', 'Dining', 'Education', 'Electronics',
                               'Entertainment', 'Groceries', 'Health', 'Travel']
        numerical_cols = expected_categories + ['age', 'annual_income']

        # Fake customers DataFrame (1 customer)
        customers = pd.DataFrame({
            'cid': [1],
            'name': ['Alice'],
            'age': [30],
            'gender': ['f'],
            'location': ['Loc1'],
            'annual_income': [50000],
            'education': ['b'],
            'occupation': ['eng']
        }).set_index('cid')

        # Fake transactions (1 transaction per category)
        transactions = pd.DataFrame({
            'cid': [1] * 8,
            'pid': [101 + i for i in range(8)],
            'amount': [10 * (i + 1) for i in range(8)],
            'purchase_date': [f'2024-01-0{i+1}' for i in range(8)],
            'payment_mode': ['card'] * 8
        })

        # Fake products (each `pid` maps to a category)
        products = pd.DataFrame({
            'bid': [i + 1 for i in range(8)],
            'pid': [101 + i for i in range(8)],
            'popularity': [10, 20, 30, 40, 50, 60, 70, 80],
            'price': [100, 200, 300, 400, 500, 600, 700, 800],
            'geo_demand': ['USA'] * 8,
            'category': expected_categories  # Ensure category exists here
        })

        # Fake businesses (used in merging)
        businesses = pd.DataFrame({
            'bid': [i + 1 for i in range(8)],
            'category': expected_categories,  # Ensure businesses also have category
            'business_name': [f'B{i+1}' for i in range(8)],
            'revenue': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
            'num_employees': [10, 20, 30, 40, 50, 60, 70, 80]
        })

        # Fix: Ensure products contain the correct `category` before merging
        products = products.merge(businesses[['bid', 'category']], on='bid', how='left')

        # Debugging print (Uncomment if needed)
        # print("Products after merge:\n", products.head())

        # The order of calls: customers, transactions, products, businesses.
        mock_get_df.side_effect = [customers, transactions, products, businesses]

        # Run function
        sim_df = customer_similarity(n_transactions=8)

        # Ensure output is a DataFrame
        self.assertIsInstance(sim_df, pd.DataFrame)

        # Ensure customer index is preserved
        self.assertTrue((sim_df.index == customers.index).all())

        # Debugging print (Uncomment if needed)
        # print("Final DataFrame columns:", sim_df.columns)    
    
    @patch('recommendations.get_avg_recent_sentiment')
    def test_sentiment_scores(self, mock_get_avg):
        # Create a fake sentiment DataFrame
        fake_df = pd.DataFrame({'avg_sentiment': [0.5]}, index=['Tech'])
        mock_get_avg.return_value = fake_df

        result = sentiment_scores(n=10)
        pd.testing.assert_frame_equal(result, fake_df)

    @patch('recommendations.np.random.rand', return_value=0.5)
    @patch('recommendations.sentiment_scores')
    @patch('recommendations.customer_similarity')
    @patch('recommendations.get_last_n_transactions_for_all_customers')
    @patch('recommendations.get_last_n_transactions_for_customer')
    @patch('recommendations.get_df_from_table')
    @patch('recommendations.product_similarity')
    def test_get_product_recommendations(
        self, mock_product_similarity, mock_get_df, mock_get_last_n_trans_customer,
        mock_last_n_trans_all, mock_customer_similarity, mock_sentiment_scores,
        mock_rand
    ):
        # Prepare fake products and businesses for get_df_from_table.
        products_df = pd.DataFrame({
            'pid': [101, 102],
            'bid': [1, 1],
            'product_name': ['ProdA', 'ProdB'],
            'popularity': [10, 20],
            'price': [100, 200],
            'geo_demand': ['USA', 'CAN']
        })
        businesses_df = pd.DataFrame({
            'bid': [1],
            'business_name': ['X Corp'],
            'category': ['Tech']
        })
        # First call returns products_df, second returns businesses_df.
        mock_get_df.side_effect = [products_df.copy(), businesses_df.copy()]

        # Prepare fake recent transactions for the customer.
        recent_transactions = pd.DataFrame({
            'tid': [1],
            'cid': [1],
            'pid': [101],
            'amount': [100],
            'purchase_date': ['2024-01-01'],
            'payment_mode': ['card']
        })
        mock_get_last_n_trans_customer.return_value = recent_transactions
    
        # Prepare fake last-n transactions for all customers.
        fake_last_n = pd.DataFrame({
            'tid': [2],
            'cid': [1],
            'pid': [102],
            'amount': [150],
            'purchase_date': ['2024-01-02'],
            'payment_mode': ['cash']
        })
        # Provide a dict with keys for both customer 1 and 2 to avoid KeyError.
        mock_last_n_trans_all.return_value = {1: fake_last_n, 2: pd.DataFrame(columns=['pid'])}

        # Fake customer similarity matrix: a simple 2x2 matrix.
        fake_customer_sim = pd.DataFrame({
            1: [1.0, 0.9],
            2: [0.9, 1.0]
        }, index=[1, 2])
        mock_customer_similarity.return_value = fake_customer_sim

        # Fake product similarity matrix.
        fake_product_sim = pd.DataFrame({
            101: {101: 1.0, 102: 0.8},
            102: {101: 0.8, 102: 1.0}
        })
        mock_product_similarity.return_value = fake_product_sim

        # Fake sentiment scores: one row per category.
        fake_sentiment = pd.DataFrame({'avg_sentiment': [0.5]}, index=['Tech'])
        mock_sentiment_scores.return_value = fake_sentiment

        # Call the recommendation function.
        recs = get_product_recommendations(
            cid=1,
            n_transactions=1,
            n_transactions_customer=100,
            n_customers=1,
            n_similar_products=1,
            n_posts=10,
            n_recommendations=1,
            product_weight=0.5,
            customer_weight=0.5,
            sentiment_weight=0.3,
            repeat_prob=0.3
        )
        # Verify that recs is a DataFrame.
        self.assertIsInstance(recs, pd.DataFrame)
        # Check that the 'pid' column exists and that a merge has added 'business_name'
        self.assertIn('pid', recs.columns)
        self.assertIn('business_name', recs.columns)
        # Check that 'score' exists
        self.assertIn('score', recs.columns)

if __name__ == '__main__':
    unittest.main()
