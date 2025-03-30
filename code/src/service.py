from database import search_products_by_name, validate_user, get_product_revenue_info, get_payment_mode_revenue_info
from models import LoginData, UserType, BusinessInsight, ProductRevenue, PaymentModeRevenue, BusinessChart
from fastapi import HTTPException
from business_insightgen import generate_insights

def search_products_service(query: str):
    results = search_products_by_name(query, as_df=True)
    return results.to_dict('records')

def authenticate_user_service(login_data: LoginData):
    is_valid_username = len(login_data.username) > 1 and (login_data.username.startswith('c') or login_data.username.startswith('b')) and login_data.username[1:].isdigit() and not login_data.username[1:].startswith('0')
    if is_valid_username:
        user_id = int(login_data.username[1:])
        user_type = UserType.CUSTOMER if login_data.username.startswith('c') else UserType.BUSINESS
        user_object = validate_user(user_id, login_data.password, user_type)
        return is_valid_username, user_object
    else:
        return False, None

def get_business_insight(bid: int):
    generation_status, result = generate_insights(bid)
    if not generation_status:
        raise HTTPException(status_code=503, detail=result)
    insights_list = result.split('\n')
    if len(insights_list) < 7:
        raise HTTPException(status_code=503, detail="Service is not available. Please try again later.")
    else:
        return BusinessInsight(action_items=insights_list[:3],questions=insights_list[4:7])
    
def get_business_kpi(bid: int):
    product_revenue_data = get_product_revenue_info(bid)
    product_revenue_list = [ProductRevenue(product_name=row[0], amount=row[1]) for row in product_revenue_data]
    payment_mode_revenue_data = get_payment_mode_revenue_info(bid)
    payment_mode_revenue_list = [PaymentModeRevenue(mode=row[0], amount=row[1]) for row in payment_mode_revenue_data]
    return BusinessChart(products=product_revenue_list, payment_mode=payment_mode_revenue_list)
