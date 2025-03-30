from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import pytest
from fastapi import HTTPException
import pandas as pd
from api import router

client = TestClient(router)

def test_search_products():
    mock_search_products_service = Mock()
    expected_result = [
        {
            "pid": 9,
            "bid": 9,
            "product_name": "Smartphone",
            "business_name": "Gallagher PLC",
            "popularity": 7,
            "price": 1344.77,
            "geo_demand": "Josephtown",
            "category": "Electronics"
        },
        {
            "pid": 19,
            "bid": 9,
            "product_name": "Smartwatch",
            "business_name": "Gallagher PLC",
            "popularity": 9.6,
            "price": 1763.4,
            "geo_demand": "Jacksonton",
            "category": "Electronics"
        },
        {
            "pid": 29,
            "bid": 9,
            "product_name": "Smartphone",
            "business_name": "Gallagher PLC",
            "popularity": 1.1,
            "price": 1548.81,
            "geo_demand": "Lake Kennethmouth",
            "category": "Electronics"
        }
    ]
    mock_search_products_service.return_value = expected_result
    with patch('api.search_products_service', mock_search_products_service):
        response = client.get("/search_products?query=smart")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_recommend_product_success():
    expected_result = [
        {
            "pid": 9,
            "bid": 9,
            "product_name": "Smartphone",
            "business_name": "Gallagher PLC",
            "popularity": 7,
            "price": 1344.77,
            "geo_demand": "Josephtown",
            "category": "Electronics"
        },
        {
            "pid": 19,
            "bid": 9,
            "product_name": "Smartwatch",
            "business_name": "Gallagher PLC",
            "popularity": 9.6,
            "price": 1763.4,
            "geo_demand": "Jacksonton",
            "category": "Electronics"
        },
        {
            "pid": 29,
            "bid": 9,
            "product_name": "Smartphone",
            "business_name": "Gallagher PLC",
            "popularity": 1.1,
            "price": 1548.81,
            "geo_demand": "Lake Kennethmouth",
            "category": "Electronics"
        }
    ]
    mock_get_customer_by_cid = Mock()
    mock_get_customer_by_cid.return_value = pd.DataFrame([{'cid': 1}])
    mock_get_product_recommendations = Mock()
    mock_get_product_recommendations.return_value = pd.DataFrame(expected_result)

    with patch('api.get_customer_by_cid', mock_get_customer_by_cid), patch('api.get_product_recommendations', mock_get_product_recommendations):
        response = client.get("/recommend?cid=1")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_recommend_product_customer_not_found():
    mock_get_customer_by_cid = Mock()
    mock_get_customer_by_cid.return_value = pd.DataFrame()

    with patch('api.get_customer_by_cid', mock_get_customer_by_cid):
        with pytest.raises(HTTPException) as e:
            response = client.get("/recommend?cid=0")
            assert response.status_code == 404
            assert response.json() == {'detail': 'Customer not found'}

def test_login_success():
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
    mock_authenticate_user_service = Mock()
    mock_authenticate_user_service.return_value = (True, user_info)

    with patch('api.authenticate_user_service', mock_authenticate_user_service):
        response = client.post("/login", json={'username': 'c1', 'password': 'testpassword'})
        assert response.status_code == 200
        assert response.json() == user_info

def test_login_failure():
    mock_authenticate_user_service = Mock()
    mock_authenticate_user_service.return_value = (False, None)

    with patch('api.authenticate_user_service', mock_authenticate_user_service):
        with pytest.raises(HTTPException) as e:
            response = client.post("/login", json={'username': 'testuser', 'password': 'wrongpassword'})
            assert response.status_code == 401
            assert response.json() == {'detail': 'Incorrect username or password'}

def test_generate_customer_chart():
    expected_result = {
        "category": [
            {
            "category": "Clothing",
            "spend": 1037.88
            },
            {
            "category": "Dining",
            "spend": 202.04999999999998
            },
            {
            "category": "Education",
            "spend": 991.05
            },
            {
            "category": "Electronics",
            "spend": 11306.32
            },
            {
            "category": "Entertainment",
            "spend": 1306.72
            },
            {
            "category": "Health",
            "spend": 1422.6699999999998
            }
        ],
        "payment_mode": [
            {
            "mode": "Credit",
            "spend": 12583.87
            },
            {
            "mode": "Debit",
            "spend": 716.5500000000001
            },
            {
            "mode": "Net Banking",
            "spend": 206.82
            },
            {
            "mode": "Wire Transfer",
            "spend": 2759.4500000000003
            }
        ]
    }
    mock_get_category_and_payment_summary = Mock()
    mock_get_category_and_payment_summary.return_value = expected_result
    with patch('api.get_category_and_payment_summary', mock_get_category_and_payment_summary):
        response = client.get("/customer_chart?cid=1")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_generate_loan_recommendation():
    expected_result = [
        {
            "loan_product_id": 18,
            "approval_probability": 0.782360315322876,
            "loan_type": "eco_friendly",
            "purchase_category": "Health",
            "min_interest_rate": 3,
            "max_interest_rate": 7,
            "min_term_months": 12,
            "max_term_months": 60,
            "min_loan_amount": 5000,
            "max_loan_amount": 50000,
            "processing_fee": 572.28,
            "loan_type_readable": "Eco Friendly Loan"
        },
        {
            "loan_product_id": 2,
            "approval_probability": 0.6812319755554199,
            "loan_type": "auto",
            "purchase_category": "Travel",
            "min_interest_rate": 3,
            "max_interest_rate": 8,
            "min_term_months": 24,
            "max_term_months": 84,
            "min_loan_amount": 10000,
            "max_loan_amount": 50000,
            "processing_fee": 955.64,
            "loan_type_readable": "Auto Loan"
        },
        {
            "loan_product_id": 12,
            "approval_probability": 0.6532388925552368,
            "loan_type": "medical",
            "purchase_category": "Health",
            "min_interest_rate": 4,
            "max_interest_rate": 10,
            "min_term_months": 12,
            "max_term_months": 48,
            "min_loan_amount": 2000,
            "max_loan_amount": 40000,
            "processing_fee": 972.92,
            "loan_type_readable": "Medical Loan"
        },
        {
            "loan_product_id": 1,
            "approval_probability": 0.4966118335723877,
            "loan_type": "personal",
            "purchase_category": "Entertainment",
            "min_interest_rate": 5,
            "max_interest_rate": 15,
            "min_term_months": 12,
            "max_term_months": 60,
            "min_loan_amount": 2000,
            "max_loan_amount": 30000,
            "processing_fee": 437.09,
            "loan_type_readable": "Personal Loan"
        },
        {
            "loan_product_id": 4,
            "approval_probability": 0.4966118335723877,
            "loan_type": "education",
            "purchase_category": "Education",
            "min_interest_rate": 4,
            "max_interest_rate": 10,
            "min_term_months": 24,
            "max_term_months": 120,
            "min_loan_amount": 5000,
            "max_loan_amount": 40000,
            "processing_fee": 638.79,
            "loan_type_readable": "Education Loan"
        },
        {
            "loan_product_id": 3,
            "approval_probability": 0.4966118335723877,
            "loan_type": "home",
            "purchase_category": "Groceries",
            "min_interest_rate": 2.5,
            "max_interest_rate": 5,
            "min_term_months": 120,
            "max_term_months": 360,
            "min_loan_amount": 100000,
            "max_loan_amount": 500000,
            "processing_fee": 758.79,
            "loan_type_readable": "Home Loan"
        }
    ]
    mock_recommend_loan = Mock()
    mock_recommend_loan.return_value = pd.DataFrame(expected_result)

    with patch('api.recommend_loan', mock_recommend_loan):
        response = client.get("/loan_recommend?cid=1")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_generate_business_insight_success():
    expected_result = {
        "action_items": [
            "action1", "action2", "action3"
        ],
        "questions": [
            "question1", "question2", "question3"
        ]
    }
    mock_get_business_by_bid = Mock()
    mock_get_business_by_bid.return_value = pd.DataFrame([{'bid': 1}])
    mock_get_business_insight = Mock()
    mock_get_business_insight.return_value = expected_result

    with patch('api.get_business_by_bid', mock_get_business_by_bid), patch('api.get_business_insight', mock_get_business_insight):
        response = client.get("/business_insight?bid=1")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_generate_business_insight_not_found():
    mock_get_business_by_bid = Mock()
    mock_get_business_by_bid.return_value = pd.DataFrame()

    with patch('api.get_business_by_bid', mock_get_business_by_bid):
        with pytest.raises(HTTPException) as e:
            response = client.get("/business_insight?bid=0")
            assert response.status_code == 404
            assert response.json() == {'detail': 'Business not found'}

def test_generate_business_chart_success():
    expected_result = {
        "products": [
            {
            "product_name": "Wireless Earbuds",
            "amount": 4709983.11
            },
            {
            "product_name": "Gaming Console",
            "amount": 2288297.13
            },
            {
            "product_name": "Laptop",
            "amount": 1123049.19
            }
        ],
        "payment_mode": [
            {
            "mode": "Credit",
            "amount": 1986691.79
            },
            {
            "mode": "Debit",
            "amount": 2025098.31
            },
            {
            "mode": "Net Banking",
            "amount": 1950899.83
            },
            {
            "mode": "Wire Transfer",
            "amount": 2158639.5
            }
        ]
    }
    mock_get_business_by_bid = Mock()
    mock_get_business_by_bid.return_value = pd.DataFrame([{'bid': 1}])
    mock_get_business_kpi = Mock()
    mock_get_business_kpi.return_value = expected_result

    with patch('api.get_business_by_bid', mock_get_business_by_bid), patch('api.get_business_kpi', mock_get_business_kpi):
        response = client.get("/business_chart?bid=1")
        assert response.status_code == 200
        assert response.json() == expected_result

def test_generate_business_chart_not_found():
    mock_get_business_by_bid = Mock()
    mock_get_business_by_bid.return_value = pd.DataFrame()

    with patch('api.get_business_by_bid', mock_get_business_by_bid):
        with pytest.raises(HTTPException) as e:
            response = client.get("/business_chart?bid=1")
            assert response.status_code == 404
            assert response.json() == {'detail': 'Business not found'}