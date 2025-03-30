import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


# Import the modules under test.
import business_insightgen
import llm_chat
from google.genai import errors  # used in llm_chat tests
from models import UserType

class DummyResponse:
    def __init__(self, error_message):
        self.body_segments = [{"error": {"message": error_message}}]
    def get(self, key, default=None):
        # Not actually used in this case, but provided for completeness.
        return getattr(self, key, default)

class TestBusinessInsightgen(unittest.TestCase):
    @patch('business_insightgen.get_df_from_table')
    @patch('business_insightgen.prompt_model')
    def test_generate_insights(self, mock_prompt_model, mock_get_df):
        # Set up dummy data for each call to get_df_from_table.
        # Call 1: businesses DataFrame
        businesses_df = pd.DataFrame([
            {"bid": 1, "category": "Tech", "other": "Business Info"}
        ])
        # Call 2: products DataFrame
        products_df = pd.DataFrame([
            {"bid": 1, "pid": 10, "product_name": "Product A", "popularity": 5.0, 
             "price": 100.0, "geo_demand": "USA"}
        ])
        # Call 3: social_media DataFrame
        social_media_df = pd.DataFrame([
            {"category": "Tech", "sentiment_score": 0.5}
        ])
        # Call 4: customers DataFrame
        customers_df = pd.DataFrame([
            {"cid": 100, "age": 30, "gender": "m", "annual_income": 60000, "education": "b"}
        ])
        # Call 5: transactions DataFrame
        transactions_df = pd.DataFrame([
            {"pid": 10, "cid": 100, "amount": 200.0}
        ])
        # Setup side_effect to return these in order.
        mock_get_df.side_effect = [businesses_df, products_df, social_media_df, customers_df, transactions_df]
        
        # Setup prompt_model to return a normal response.
        mock_prompt_model.return_value = (True, "Generated output")
        
        # Call generate_insights with bid = 1.
        status, result = business_insightgen.generate_insights(1)
        
        # Assert that the final output is as expected.
        self.assertTrue(status)
        self.assertEqual(result, "Generated output")
        
        # Verify that get_df_from_table was called 5 times.
        self.assertEqual(mock_get_df.call_count, 5)
        
        # Verify that prompt_model was called once.
        mock_prompt_model.assert_called_once()
        
        # Additionally, ensure that the aggregated prompt contains key substrings:
        prompt_arg = mock_prompt_model.call_args[0][0]
        self.assertIn("Business Data:", prompt_arg)
        self.assertIn("Customer Data:", prompt_arg)
        self.assertIn("Product Data:", prompt_arg)
        self.assertIn("Social Media Data:", prompt_arg)
        self.assertIn("Action item", prompt_arg)  # Though not literal, instructions are present

class TestLLMChat(unittest.TestCase):
    @patch('llm_chat.client.models.generate_content')
    def test_prompt_model_success(self, mock_generate_content):
        # Simulate a normal response.
        response_mock = MagicMock()
        response_mock.text = "Test output"
        mock_generate_content.return_value = response_mock
        
        prompt = "Test prompt\nLine two"
        status, result = llm_chat.prompt_model(prompt)
        
        self.assertTrue(status)
        self.assertEqual(result, "Test output")
        # Verify that generate_content was called with splitlines() of the prompt.
        mock_generate_content.assert_called_with(
            model="gemini-2.0-flash", contents=prompt.splitlines()
        )

    @patch('llm_chat.client.models.generate_content')
    def test_prompt_model_api_error(self, mock_generate_content):
        error_message = "API error occurred"
        dummy_response = DummyResponse(error_message)
        # Raise APIError with our dummy response.
        mock_generate_content.side_effect = errors.APIError(error_message, dummy_response)
        
        prompt = "Test prompt\nLine two"
        status, result = llm_chat.prompt_model(prompt)
        
        self.assertFalse(status)
        self.assertEqual(result, error_message)

if __name__ == '__main__':
    unittest.main()
