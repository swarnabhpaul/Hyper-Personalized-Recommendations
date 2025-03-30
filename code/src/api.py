from fastapi import APIRouter, Query, HTTPException
from typing import List
from models import Product, LoginData, CustomerChart, BusinessInsight, BusinessChart
from service import search_products_service, authenticate_user_service, get_business_insight, get_business_kpi
from recommendations import get_product_recommendations
from database import get_customer_by_cid, get_category_and_payment_summary, get_business_by_bid
from loan_recommendation import recommend_loan
import datetime

router = APIRouter()

@router.get("/search_products", response_model=List[Product])
async def search_products(query: str = Query(..., min_length=1)):
    return search_products_service(query)

@router.get("/recommend", response_model=List[Product])
async def recommend_product(cid: int = Query(...)):
    customer = get_customer_by_cid(cid, as_df=True)
    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    df = get_product_recommendations(cid)
    return df.to_dict('records')

@router.post("/login", response_model=None)
async def login(login_data: LoginData):
    is_valid_username, user_object = authenticate_user_service(login_data)
    if is_valid_username and user_object:
        return user_object
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.get("/customer_chart", response_model = CustomerChart)
async def generate_customer_chart(cid: int = Query(...)):
    customer_chart = get_category_and_payment_summary(cid)
    return customer_chart

@router.get("/loan_recommend")
async def generate_loan_recommendation(cid: int = Query(...)):
    df = recommend_loan(cid)
    return df.to_dict('records')

@router.get("/business_insight", response_model=BusinessInsight)
async def generate_business_insight(bid: int = Query(...)):
    business = get_business_by_bid(bid, as_df=True)
    if business.empty:
        raise HTTPException(status_code=404, detail="Business not found")
    insight = get_business_insight(bid)
    return insight

@router.get("/business_chart", response_model = BusinessChart)
async def generate_business_chart(bid: int = Query(...)):
    business = get_business_by_bid(bid, as_df=True)
    if business.empty:
        raise HTTPException(status_code=404, detail="Business not found")
    business_chart = get_business_kpi(bid)
    return business_chart