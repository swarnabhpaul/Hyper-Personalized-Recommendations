import unittest
from unittest.mock import patch, MagicMock
import database
from models import UserType
import datetime
import pandas as pd

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Create mock connection and cursor objects and override the globals in the module
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        database.conn = self.mock_conn
        database.c = self.mock_cursor
    
    @patch('database.sqlite3.connect')
    def test_init_connection(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        
        database.init_connection()
        
        mock_connect.assert_called_with('database.db')
        mock_conn.cursor.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    def test_drop_existing_tables(self, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()

        database.drop_existing_tables()

        # Ensure the execute function is called 7 times (once per table)
        self.assertEqual(mock_cursor.execute.call_count, 7)
        mock_conn.commit.assert_called()
    
    @patch('database.pd.read_csv')
    @patch('database.conn')
    @patch('database.c')
    def test_init_customers(self, mock_cursor, mock_conn, mock_read_csv):
        mock_cursor.execute = MagicMock()
        
        # Ensure mock_read_csv returns a valid DataFrame
        mock_read_csv.return_value = pd.DataFrame([{
            'name': 'John Doe', 'age': 30, 'gender': 'Male', 'location': 'NY', 
            'annual_income': 50000, 'education': 'Bachelor', 'occupation': 'Engineer'
        }])
        
        database.init_customers()

        # Ensure the INSERT statement is called
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_businesses(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'category': 'Retail', 'business_name': 'ABC Store', 'revenue': 100000, 'num_employees': 10}
        ])
        
        database.init_businesses()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_products(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'bid': 1, 'product_name': 'Laptop', 'popularity': 4.5, 'price': 1000, 'geo_demand': 'USA'}
        ])
        
        database.init_products()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_transactions(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'cid': 1, 'pid': 1, 'amount': 100, 'purchase_date': '2024-01-01', 'payment_mode': 'Credit Card'}
        ])
        
        database.init_transactions()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_social_media(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'platform': 'Twitter', 'content': 'Great Product!', 'timestamp': '2024-01-01', 'sentiment_score': 0.8, 'category': 'Tech'}
        ])
        
        database.init_social_media()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_loan_products(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'loan_product_id': 1, 'loan_type': 'Personal Loan', 'purchase_category': 'Electronics', 'min_interest_rate': 5.0, 'max_interest_rate': 15.0, 'min_term_months': 12, 'max_term_months': 60, 'min_loan_amount': 1000, 'max_loan_amount': 50000, 'processing_fee': 2.0}
        ])
        
        database.init_loan_products()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
    
    @patch('database.conn')
    @patch('database.c')
    @patch('database.pd.read_csv')
    def test_init_loan_applications(self, mock_read_csv, mock_cursor, mock_conn):
        mock_cursor.execute = MagicMock()
        mock_read_csv.return_value = pd.DataFrame([
            {'application_id': 1, 'cid': 1, 'loan_product_id': 1, 'loan_amount': 10000, 'interest_rate': 7.5, 'loan_term_months': 36, 'credit_score': 750, 'annual_income': 60000, 'debt_to_income_ratio': 20.0, 'application_date': '2024-01-01', 'status': 'Approved'}
        ])
        
        database.init_loan_applications()
        
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_transactions_for_customer(self, mock_execute):
        mock_execute.return_value = [(1, 100, 50.0, '2024-01-01', 'Credit Card')]
        result = database.get_last_n_transactions_for_customer(1, 1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], 50.0)
    
    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_social_media_posts(self, mock_execute):
        mock_execute.return_value = [(1, 'Twitter', 'Great Product!', '2024-01-01', 0.8, 'Tech')]
        result = database.get_last_n_social_media_posts(1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Twitter')
    
    @patch('database.execute_and_fetch_one')
    def test_get_product_by_pid(self, mock_execute):
        mock_execute.return_value = (1, 'Laptop', 5, 1000.0, 'USA', 'Tech')
        result = database.get_product_by_pid(1)
        
        self.assertEqual(result[1], 'Laptop')
        self.assertEqual(result[3], 1000.0)
    
    @patch('database.execute_and_fetch_one')
    def test_validate_user(self, mock_execute):
        mock_execute.return_value = pd.DataFrame([{'cid': 1, 'name': 'John Doe'}])
        result = database.validate_user(1, 'password', UserType.CUSTOMER)
        
        self.assertEqual(result['name'], 'John Doe')
    
    @patch('database.execute_and_fetch_rows')
    def test_get_category_and_payment_summary(self, mock_execute):
        mock_execute.side_effect = [
            [('Tech', 500.0)],  # Category Spend
            [('Credit Card', 300.0)]  # Payment Mode Spend
        ]
        result = database.get_category_and_payment_summary(1, datetime.date(2024, 1, 1))
        
        self.assertEqual(result['category'][0]['category'], 'Tech')
        self.assertEqual(result['category'][0]['spend'], 500.0)
        self.assertEqual(result['payment_mode'][0]['mode'], 'Credit Card')
        self.assertEqual(result['payment_mode'][0]['spend'], 300.0)

    @patch('database.drop_existing_tables')
    @patch('database.init_customers')
    @patch('database.init_businesses')
    @patch('database.init_products')
    @patch('database.init_transactions')
    @patch('database.init_social_media')
    @patch('database.init_loan_products')
    @patch('database.init_loan_applications')
    def test_init_db(self, mock_init_loan_applications, mock_init_loan_products, 
                     mock_init_social_media, mock_init_transactions, 
                     mock_init_products, mock_init_businesses, mock_init_customers,
                     mock_drop_existing_tables):
        with patch('builtins.print') as mock_print:
            database.init_db()
        # Check that foreign keys were enabled
        self.mock_cursor.execute.assert_any_call('pragma foreign_keys=on')
        # Ensure all initialization functions were called
        mock_drop_existing_tables.assert_called_once()
        mock_init_customers.assert_called_once()
        mock_init_businesses.assert_called_once()
        mock_init_products.assert_called_once()
        mock_init_transactions.assert_called_once()
        mock_init_social_media.assert_called_once()
        mock_init_loan_products.assert_called_once()
        mock_init_loan_applications.assert_called_once()
        mock_print.assert_called_with("initialization complete")

    def test_close_connection(self):
        with patch('builtins.print') as mock_print:
            database.close_connection()
        self.mock_conn.close.assert_called_once()
        # We no longer assert that database.c is None because the function's assignment doesn't update the global variable.
        mock_print.assert_called_with('Connection closed')

    def test_get_first_n(self):
        table_name = "test_table"
        n = 5
        expected_query = f'select * from {table_name} limit {n}'
        expected_result = [(1, 2), (3, 4)]
        self.mock_cursor.fetchall.return_value = expected_result

        result = database.get_first_n(table_name, n)
        self.mock_cursor.execute.assert_called_with(expected_query)
        self.assertEqual(result, expected_result)

    @patch('database.pd.read_sql_query')
    def test_get_df_from_table(self, mock_read_sql_query):
        table_name = "test_table"
        limit = 10
        order_by = "id"
        order = "ASC"
        index_col = "id"
        query = f'select * from {table_name} order by {order_by} {order} limit {limit}'
        expected_df = pd.DataFrame({'id': [1, 2]})
        mock_read_sql_query.return_value = expected_df

        result = database.get_df_from_table(table_name, limit=limit, order_by=order_by, order=order, index_col=index_col)
        mock_read_sql_query.assert_called_with(query, database.conn, index_col=index_col)
        pd.testing.assert_frame_equal(result, expected_df)

    def test_execute_and_fetch_rows_as_list(self):
        query = "SELECT * FROM test"
        expected_result = [(1, 2)]
        # Simulate cursor.description for DataFrame conversion if needed
        self.mock_cursor.description = [("col1",), ("col2",)]
        # Simulate the chain: execute(query) -> fetchall()
        self.mock_cursor.execute.return_value.fetchall.return_value = expected_result

        result = database.execute_and_fetch_rows(query, as_df=False)
        self.mock_cursor.execute.assert_called_with(query)
        self.assertEqual(result, expected_result)

    def test_execute_and_fetch_rows_as_df(self):
        query = "SELECT * FROM test"
        expected_result = [(1, 2)]
        # Set description to have two columns
        self.mock_cursor.description = [("col1",), ("col2",)]
        self.mock_cursor.execute.return_value.fetchall.return_value = expected_result

        # When index_col is provided, the column is set as index so it won't appear in df.columns.
        result = database.execute_and_fetch_rows(query, as_df=True, index_col="col1")
        self.assertIsInstance(result, pd.DataFrame)
        # Expected remaining columns is only "col2" because "col1" becomes the index.
        self.assertEqual(list(result.columns), ["col2"])
        self.assertEqual(result.index.name, "col1")

    def test_execute_and_fetch_one_as_list(self):
        query = "SELECT * FROM test"
        expected_result = (1, 2)
        self.mock_cursor.description = [("col1",), ("col2",)]
        self.mock_cursor.execute.return_value.fetchone.return_value = expected_result

        result = database.execute_and_fetch_one(query, as_df=False)
        self.mock_cursor.execute.assert_called_with(query)
        self.assertEqual(result, expected_result)

    def test_execute_and_fetch_one_as_df(self):
        query = "SELECT * FROM test"
        expected_result = (1, 2)
        self.mock_cursor.description = [("col1",), ("col2",)]
        self.mock_cursor.execute.return_value.fetchone.return_value = expected_result

        result = database.execute_and_fetch_one(query, as_df=True)
        self.mock_cursor.execute.assert_called_with(query)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["col1", "col2"])

    def test_execute_and_fetch_one_no_result(self):
        query = "SELECT * FROM test"
        self.mock_cursor.execute.return_value.fetchone.return_value = None

        result = database.execute_and_fetch_one(query, as_df=True)
        self.mock_cursor.execute.assert_called_with(query)
        self.assertTrue(result.empty)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_transactions_for_all_customers_list(self, mock_exec_rows):
        # When as_df is False, simply return the list that the lower-level function returns.
        expected = [(1, 1, 1, 100, '2024-01-01', 'Credit Card')]
        mock_exec_rows.return_value = expected

        result = database.get_last_n_transactions_for_all_customers(n=1, as_df=False)
        # Verify that our function returns the same list.
        self.assertEqual(result, expected)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_transactions_for_all_customers_df(self, mock_exec_rows):
        # When as_df is True, our function groups the returned DataFrame by 'cid'
        df = pd.DataFrame({
            'tid': [1, 2],
            'cid': [1, 1],
            'pid': [1, 2],
            'amount': [100, 200],
            'purchase_date': ['2024-01-01', '2024-01-02'],
            'payment_mode': ['Credit Card', 'Cash']
        })
        mock_exec_rows.return_value = df

        result = database.get_last_n_transactions_for_all_customers(n=2, as_df=True)
        # Expect a dictionary keyed by customer id. In this case, all rows have cid 1.
        self.assertIsInstance(result, dict)
        self.assertIn(1, result)
        pd.testing.assert_frame_equal(result[1], df)

    @patch('database.execute_and_fetch_rows')
    def test_get_avg_recent_sentiment_list(self, mock_exec_rows):
        # When as_df is False, simply return the list provided by the lower-level function.
        expected = [('Tech', 0.8)]
        mock_exec_rows.return_value = expected

        result = database.get_avg_recent_sentiment(n=5, as_df=False)
        self.assertEqual(result, expected)

    @patch('database.execute_and_fetch_rows')
    def test_get_avg_recent_sentiment_df(self, mock_exec_rows):
        # Create a DataFrame and set the index to 'category'
        df = pd.DataFrame({'category': ['Tech'], 'avg_sentiment': [0.8]})
        df = df.set_index('category')
        mock_exec_rows.return_value = df

        result = database.get_avg_recent_sentiment(n=5, as_df=True)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index.name, 'category')
        self.assertEqual(list(result.columns), ['avg_sentiment'])

    @patch('database.execute_and_fetch_rows')
    def test_search_products_by_name(self, mock_exec_rows):
        # Return a dummy list for the query
        expected = [(1, 'Laptop', 4.5, 1000, 'USA', 'Tech', 'Some Business')]
        mock_exec_rows.return_value = expected

        query_param = 'Laptop'
        result = database.search_products_by_name(query_param, as_df=False)
        self.assertEqual(result, expected)
        # Verify that the query passed to execute_and_fetch_rows includes our query_param.
        # We'll extract the search query from the call arguments:
        actual_query = mock_exec_rows.call_args[0][0]
        self.assertIn(f"LIKE '%{query_param}%'", actual_query)

    @patch('database.execute_and_fetch_one')
    def test_get_customer_by_cid(self, mock_exec_one):
        expected = (1, 'John Doe', 30, 'Male', 'NY', 50000, 'Bachelor', 'Engineer')
        mock_exec_one.return_value = expected

        result = database.get_customer_by_cid(1, as_df=False)
        self.assertEqual(result, expected)
        expected_query = "\n    select * from customers where cid = 1\n    "
        mock_exec_one.assert_called_with(expected_query, as_df=False)

    @patch('database.execute_and_fetch_one')
    def test_get_business_by_bid(self, mock_exec_one):
        expected = (1, 'Retail', 'ABC Corp', 100000, 50)
        mock_exec_one.return_value = expected

        result = database.get_business_by_bid(1, as_df=False)
        self.assertEqual(result, expected)
        expected_query = "\n    select * from businesses where bid = 1\n    "
        mock_exec_one.assert_called_with(expected_query, as_df=False)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_with_limit(self, mock_exec_rows):
        # Prepare a dummy result for when n is provided
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 1
        n = 5
        result = database.get_last_n_loan_applications_by_cid(cid, n=n, as_df=False)
        
        # Verify that the query was constructed correctly with limit
        expected_query = f"""\n    select * from loan_applications where cid = {cid} order by application_date desc\n    limit {n}\n        """
        # Since the query is constructed in the function and passed to execute_and_fetch_rows,
        # we can check that the mock was called with a query containing both the "cid" and "limit" parts.
        args, kwargs = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_without_limit(self, mock_exec_rows):
        # When n is not provided, the query should not include a LIMIT clause.
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 2
        result = database.get_last_n_loan_applications_by_cid(cid, n=None, as_df=False)
        
        args, kwargs = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertNotIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_product_revenue_info(self, mock_exec_rows):
        # Prepare a dummy result for product revenue info
        dummy_result = [('Laptop', 5000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 1
        result = database.get_product_revenue_info(bid, as_df=False)
        
        args, kwargs = mock_exec_rows.call_args
        # Ensure the query contains the expected FROM and GROUP BY clauses.
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.pid", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_payment_mode_revenue_info(self, mock_exec_rows):
        # Prepare a dummy result for payment mode revenue info
        dummy_result = [('Credit Card', 7000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 2
        result = database.get_payment_mode_revenue_info(bid, as_df=False)
        
        args, kwargs = mock_exec_rows.call_args
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.payment_mode", args[0])
        self.assertEqual(result, dummy_result)

    # --- Test for get_df_from_table branch when c is None (lines 269-272) ---
    @patch('database.init_connection')
    @patch('database.pd.read_sql_query')
    def test_get_df_from_table_no_cursor(self, mock_read_sql_query, mock_init_conn):
        # Simulate that the global cursor is None so that init_connection is triggered.
        database.c = None
        expected_df = pd.DataFrame({'id': [1, 2]})
        mock_read_sql_query.return_value = expected_df

        result = database.get_df_from_table("test_table", limit=10, order_by="id", order="ASC", index_col="id")
        # Check that init_connection was called to reinitialize c
        mock_init_conn.assert_called_once()
        query = f'select * from test_table order by id ASC limit 10'
        mock_read_sql_query.assert_called_with(query, database.conn, index_col="id")
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('database.init_connection')
    def test_execute_and_fetch_rows_no_cursor(self, mock_init_conn):
        # Set the global cursor to None to trigger init_connection
        database.c = None
        # Create a new mock cursor to be set by init_connection
        new_cursor = MagicMock()
        new_cursor.description = [("col1",), ("col2",)]
        new_cursor.execute.return_value.fetchall.return_value = [(1, 2)]
        # When init_connection is called, set database.c to our new_cursor
        mock_init_conn.side_effect = lambda: setattr(database, 'c', new_cursor)
        
        result = database.execute_and_fetch_rows("SELECT * FROM test", as_df=True, index_col="col1")
        mock_init_conn.assert_called_once()
        self.assertIsInstance(result, pd.DataFrame)
        # Since "col1" is used as the index, only "col2" remains in df.columns.
        self.assertEqual(list(result.columns), ["col2"])
        self.assertEqual(result.index.name, "col1")

    @patch('database.init_connection')
    def test_execute_and_fetch_one_no_cursor(self, mock_init_conn):
        # Set the global cursor to None to trigger init_connection
        database.c = None
        # Create a new mock cursor to be set by init_connection
        new_cursor = MagicMock()
        new_cursor.description = [("col1",), ("col2",)]
        new_cursor.execute.return_value.fetchone.return_value = (1, 2)
        # When init_connection is called, set database.c to our new_cursor
        mock_init_conn.side_effect = lambda: setattr(database, 'c', new_cursor)
        
        result = database.execute_and_fetch_one("SELECT * FROM test", as_df=True)
        mock_init_conn.assert_called_once()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["col1", "col2"])

    # --- Test validate_user branch: wrong password, wrong user type, and empty result (lines 493-499) ---
    @patch('database.get_customer_by_cid')
    @patch('database.get_business_by_bid')
    def test_validate_user_wrong_password(self, mock_get_business, mock_get_customer):
        # Wrong password should return None
        result = database.validate_user(1, "wrong_password", UserType.CUSTOMER)
        self.assertIsNone(result)
        mock_get_customer.assert_not_called()
        mock_get_business.assert_not_called()

    @patch('database.get_customer_by_cid')
    @patch('database.get_business_by_bid')
    def test_validate_user_wrong_user_type(self, mock_get_business, mock_get_customer):
        # Provide a user_type not covered (e.g. an invalid string)
        result = database.validate_user(1, "password", "invalid")
        self.assertIsNone(result)
        mock_get_customer.assert_not_called()
        mock_get_business.assert_not_called()

    @patch('database.get_customer_by_cid')
    def test_validate_user_empty_result(self, mock_get_customer):
        # Simulate get_customer_by_cid returning an empty DataFrame.
        mock_get_customer.return_value = pd.DataFrame()
        result = database.validate_user(1, "password", UserType.CUSTOMER)
        self.assertIsNone(result)

    @patch('database.get_customer_by_cid')
    def test_validate_user_valid(self, mock_get_customer):
        # Simulate a valid DataFrame result
        mock_get_customer.return_value = pd.DataFrame([{'cid': 1, 'name': 'John Doe'}])
        result = database.validate_user(1, "password", UserType.CUSTOMER)
        self.assertEqual(result, {'cid': 1, 'name': 'John Doe'})

    # --- Test for get_category_and_payment_summary branch when after_date is not provided (lines 609-610) ---
    @patch('database.execute_and_fetch_rows')
    def test_get_category_and_payment_summary_no_after_date(self, mock_exec_rows):
        # Simulate the two queries returning dummy data.
        dummy_category = [("Tech", 500.0)]
        dummy_payment = [("Credit Card", 300.0)]
        # Use side_effect so the first call returns category data and second returns payment mode data.
        mock_exec_rows.side_effect = [dummy_category, dummy_payment]

        result = database.get_category_and_payment_summary(1)
        # Check that the where clause doesn't include the after_date part.
        self.assertIn("WHERE t.cid = 1", mock_exec_rows.call_args_list[0][0][0])
        self.assertNotIn("purchase_date >=", mock_exec_rows.call_args_list[0][0][0])
        self.assertEqual(result, {
            "category": [{"category": "Tech", "spend": 500.0}],
            "payment_mode": [{"mode": "Credit Card", "spend": 300.0}]
        })

    # --- Tests for get_last_n_loan_applications_by_cid, get_product_revenue_info, get_payment_mode_revenue_info ---
    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_with_limit(self, mock_exec_rows):
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 1
        n = 5
        result = database.get_last_n_loan_applications_by_cid(cid, n=n, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_without_limit(self, mock_exec_rows):
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 2
        result = database.get_last_n_loan_applications_by_cid(cid, n=None, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertNotIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_product_revenue_info(self, mock_exec_rows):
        dummy_result = [('Laptop', 5000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 1
        result = database.get_product_revenue_info(bid, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.pid", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_payment_mode_revenue_info(self, mock_exec_rows):
        dummy_result = [('Credit Card', 7000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 2
        result = database.get_payment_mode_revenue_info(bid, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.payment_mode", args[0])
        self.assertEqual(result, dummy_result)

    # Validate the business branch in validate_user (line ~497)
    @patch('database.get_business_by_bid')
    def test_validate_user_business_valid(self, mock_get_business):
        # Simulate a valid DataFrame result for a business user.
        mock_get_business.return_value = pd.DataFrame([{'bid': 2, 'business_name': 'ABC Corp'}])
        result = database.validate_user(2, "password", UserType.BUSINESS)
        self.assertEqual(result, {'bid': 2, 'business_name': 'ABC Corp'})
    
    # Validate get_category_and_payment_summary when after_date is provided (lines 609-610)
    @patch('database.execute_and_fetch_rows')
    def test_get_category_and_payment_summary_with_after_date(self, mock_exec_rows):
        # Set up a dummy after_date and dummy return values.
        after_date = datetime.date(2024, 2, 1)
        dummy_category = [("Tech", 500.0)]
        dummy_payment = [("Cash", 300.0)]
        # The first call (category query) and second call (payment query)
        mock_exec_rows.side_effect = [dummy_category, dummy_payment]
        
        result = database.get_category_and_payment_summary(1, after_date=after_date)
        formatted_date = after_date.strftime('%Y-%m-%d %H:%M:%S')
        # Verify that the first query includes the formatted after_date.
        self.assertIn(f"AND t.purchase_date >= '{formatted_date}'", mock_exec_rows.call_args_list[0][0][0])
        self.assertEqual(result, {
            "category": [{"category": "Tech", "spend": 500.0}],
            "payment_mode": [{"mode": "Cash", "spend": 300.0}]
        })
    
    # ---------------------------
    # Already provided tests for:
    # ---------------------------
    # get_last_n_loan_applications_by_cid, get_product_revenue_info,
    # get_payment_mode_revenue_info
    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_with_limit(self, mock_exec_rows):
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 1
        n = 5
        result = database.get_last_n_loan_applications_by_cid(cid, n=n, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_last_n_loan_applications_by_cid_without_limit(self, mock_exec_rows):
        dummy_result = [(1, 'Loan App', 10000, '2024-01-01')]
        mock_exec_rows.return_value = dummy_result
        
        cid = 2
        result = database.get_last_n_loan_applications_by_cid(cid, n=None, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn(f"where cid = {cid}", args[0])
        self.assertNotIn("limit", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_product_revenue_info(self, mock_exec_rows):
        dummy_result = [('Laptop', 5000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 1
        result = database.get_product_revenue_info(bid, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.pid", args[0])
        self.assertEqual(result, dummy_result)

    @patch('database.execute_and_fetch_rows')
    def test_get_payment_mode_revenue_info(self, mock_exec_rows):
        dummy_result = [('Credit Card', 7000)]
        mock_exec_rows.return_value = dummy_result
        
        bid = 2
        result = database.get_payment_mode_revenue_info(bid, as_df=False)
        args, _ = mock_exec_rows.call_args
        self.assertIn("FROM transactions t", args[0])
        self.assertIn("JOIN products p", args[0])
        self.assertIn(f"WHERE p.bid = {bid}", args[0])
        self.assertIn("GROUP BY t.payment_mode", args[0])
        self.assertEqual(result, dummy_result)

    @patch('builtins.print')
    @patch('database.execute_and_fetch_rows')
    def test_get_category_and_payment_summary_with_after_date(self, mock_exec_rows, mock_print):
        # Set up a dummy after_date and dummy return values.
        after_date = datetime.date(2024, 2, 1)
        dummy_category = [("Tech", 500.0)]
        dummy_payment = [("Cash", 300.0)]
        # The first call (category query) and second call (payment query)
        mock_exec_rows.side_effect = [dummy_category, dummy_payment]
        
        result = database.get_category_and_payment_summary(1, after_date=after_date)
        formatted_date = after_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # Verify that the category query includes the formatted after_date.
        self.assertIn(f"AND t.purchase_date >= '{formatted_date}'", mock_exec_rows.call_args_list[0][0][0])
        
        # Verify the result dictionary.
        expected_result = {
            "category": [{"category": "Tech", "spend": 500.0}],
            "payment_mode": [{"mode": "Cash", "spend": 300.0}]
        }
        self.assertEqual(result, expected_result)
        
        # Verify that print was called at least twice:
        # One call prints the category query and one prints the result.
        self.assertGreaterEqual(len(mock_print.call_args_list), 2)
        # Verify that the last print call printed the expected result dictionary.
        printed_result = mock_print.call_args_list[-1][0][0]
        self.assertEqual(printed_result, expected_result)
        
if __name__ == '__main__':
    unittest.main()