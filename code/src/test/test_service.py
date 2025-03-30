import unittest
from unittest.mock import patch, Mock
from service import search_products_service, authenticate_user_service, get_business_insight, get_business_kpi
from models import LoginData, BusinessInsight, ProductRevenue, PaymentModeRevenue, BusinessChart
from fastapi import HTTPException
import pandas as pd

class TestService(unittest.TestCase):

    def test_search_products_service(self):
        expected_result = [{'pid': 1, 'bid': 1, 'product_name': 'Test', 'business_name': 'Test', 'popularity': 1.0, 'price': 10.0, 'geo_demand': 'US', 'category': 'Test'}]
        # Mock the search_products_by_name function
        with patch('service.search_products_by_name') as mock_search:
            mock_search.return_value = pd.DataFrame(expected_result)

            # Call the search_products_service function
            result = search_products_service('Test')

            # Assert the expected result
            self.assertEqual(result, expected_result)

    def test_authenticate_user_service(self):
        user_info = {
            "cid": 1,
            "name": "Jennifer Willis",
            "age": 38,
            "gender": "o",
            "location": "Port Matthew",
            "annual_income": 52562,
            "education": "m",
            "occupation": "Legal executive"
        }
        # Mock the validate_user function
        with patch('service.validate_user') as mock_validate:
            mock_validate.return_value = user_info

            # Call the authenticate_user_service function
            result = authenticate_user_service(LoginData(username='c1', password='password'))

            # Assert the expected result
            self.assertEqual(result, (True, user_info))

    def test_authenticate_user_service_invalid_username(self):
        # Mock the validate_user function
        with patch('service.validate_user') as mock_validate:
            mock_validate.return_value = None

            # Call the authenticate_user_service function with an invalid username
            result = authenticate_user_service(LoginData(username='invalid', password='password'))

            # Assert the expected result
            self.assertEqual(result, (False, None))

    def test_get_business_insight(self):
        # Mock the generate_insights and get_product_revenue_info functions
        with patch('service.generate_insights') as mock_generate:
            mock_generate.return_value = (True, "Action Item 1\nAction Item 2\nAction Item 3\n\nQuestion 1\nQuestion 2\nQuestion 3")

            # Call the get_business_insight function
            result = get_business_insight(1)

            # Assert the expected result
            self.assertEqual(result, BusinessInsight(action_items=['Action Item 1', 'Action Item 2', 'Action Item 3'], questions=['Question 1', 'Question 2', 'Question 3']))

    def test_get_business_insight_service_unavailable(self):
        # Mock the generate_insights function
        with patch('service.generate_insights') as mock_generate:
            mock_generate.return_value = (False, "Service is not available. Please try again later.")

            # Call the get_business_insight function
            with self.assertRaises(HTTPException) as cm:
                get_business_insight(1)

            # Assert the expected HTTPException status code and detail
            self.assertEqual(cm.exception.status_code, 503)
            self.assertEqual(cm.exception.detail, "Service is not available. Please try again later.")

    def test_get_business_insight_service_insufficient_insights(self):
        # Mock the generate_insights function
        with patch('service.generate_insights') as mock_generate:
            mock_generate.return_value = (True, "Action Item 1\nAction Item 2\n")

            # Call the get_business_insight function
            with self.assertRaises(HTTPException) as cm:
                get_business_insight(1)

            # Assert the expected HTTPException status code and detail
            self.assertEqual(cm.exception.status_code, 503)
            self.assertEqual(cm.exception.detail, "Service is not available. Please try again later.")

    def test_get_business_kpi(self):
        # Mock the get_product_revenue_info and get_payment_mode_revenue_info functions
        with patch('service.get_product_revenue_info') as mock_product_revenue, patch('service.get_payment_mode_revenue_info') as mock_payment_mode_revenue:
            mock_product_revenue.return_value = [('Product 1', 100.0), ('Product 2', 200.0)]
            mock_payment_mode_revenue.return_value = [('Mode 1', 500.0), ('Mode 2', 300.0)]

            # Call the get_business_kpi function
            result = get_business_kpi(1)

            # Assert the expected result
            self.assertEqual(result, BusinessChart(products=[ProductRevenue(product_name='Product 1', amount=100.0), ProductRevenue(product_name='Product 2', amount=200.0)], payment_mode=[PaymentModeRevenue(mode='Mode 1', amount=500.0), PaymentModeRevenue(mode='Mode 2', amount=300.0)]))

if __name__ == '__main__':
    unittest.main()