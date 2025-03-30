import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse

# Set random seed for reproducibility
np.random.seed(42)

parser = argparse.ArgumentParser(description='Generate synthetic loan data.')
parser.add_argument('--num_customers', type=int, default=10000, help='Number of customers')
parser.add_argument('--num_applications', type=int, default=100000, help='Number of historical loan applications')
args = parser.parse_args()

# Define 20 loan types and their associated parameters:
loan_details = {
    'personal': {'interest_range': (5.0, 15.0), 'term_range': (12, 60), 'loan_amount_range': (2000, 30000)},
    'auto': {'interest_range': (3.0, 8.0), 'term_range': (24, 84), 'loan_amount_range': (10000, 50000)},
    'home': {'interest_range': (2.5, 5.0), 'term_range': (120, 360), 'loan_amount_range': (100000, 500000)},
    'education': {'interest_range': (4.0, 10.0), 'term_range': (24, 120), 'loan_amount_range': (5000, 40000)},
    'business': {'interest_range': (5.0, 12.0), 'term_range': (12, 120), 'loan_amount_range': (5000, 200000)},
    'small_business': {'interest_range': (6.0, 14.0), 'term_range': (12, 84), 'loan_amount_range': (10000, 150000)},
    'agricultural': {'interest_range': (4.5, 9.0), 'term_range': (24, 120), 'loan_amount_range': (20000, 300000)},
    'student': {'interest_range': (3.5, 8.0), 'term_range': (60, 240), 'loan_amount_range': (5000, 50000)},
    'mortgage': {'interest_range': (2.5, 5.0), 'term_range': (120, 360), 'loan_amount_range': (100000, 1000000)},
    'credit_builder': {'interest_range': (7.0, 18.0), 'term_range': (6, 36), 'loan_amount_range': (500, 5000)},
    'debt_consolidation': {'interest_range': (5.0, 15.0), 'term_range': (12, 60), 'loan_amount_range': (5000, 50000)},
    'medical': {'interest_range': (4.0, 10.0), 'term_range': (12, 48), 'loan_amount_range': (2000, 40000)},
    'vacation': {'interest_range': (6.0, 16.0), 'term_range': (6, 24), 'loan_amount_range': (1000, 10000)},
    'wedding': {'interest_range': (5.0, 12.0), 'term_range': (12, 36), 'loan_amount_range': (3000, 30000)},
    'refinancing': {'interest_range': (2.0, 5.0), 'term_range': (60, 360), 'loan_amount_range': (10000, 500000)},
    'construction': {'interest_range': (4.5, 9.0), 'term_range': (24, 120), 'loan_amount_range': (50000, 500000)},
    'equipment': {'interest_range': (5.0, 10.0), 'term_range': (12, 60), 'loan_amount_range': (10000, 200000)},
    'eco_friendly': {'interest_range': (3.0, 7.0), 'term_range': (12, 60), 'loan_amount_range': (5000, 50000)},
    'travel': {'interest_range': (6.0, 15.0), 'term_range': (6, 24), 'loan_amount_range': (1000, 15000)},
    'other': {'interest_range': (5.0, 15.0), 'term_range': (12, 60), 'loan_amount_range': (1000, 50000)}
}

# Logical mapping between loan types and purchase categories
loan_type_to_category = {
    'personal': 'Entertainment',       
    'auto': 'Travel',                    
    'home': 'Groceries',                 
    'education': 'Education',            
    'business': 'Electronics',           
    'small_business': 'Electronics',     
    'agricultural': 'Groceries',         
    'student': 'Education',              
    'mortgage': 'Groceries',             
    'credit_builder': 'Clothing',        
    'debt_consolidation': 'Dining',      
    'medical': 'Health',                 
    'vacation': 'Travel',                
    'wedding': 'Dining',                 
    'refinancing': 'Electronics',        
    'construction': 'Groceries',         
    'equipment': 'Electronics',          
    'eco_friendly': 'Health',            
    'travel': 'Travel',                  
    'other': 'Entertainment'             
}

# --- 1. Create Loan Product Details Dataset ---
loan_product_data = []
# For each loan type, generate one product with a unique loan_product_id from 1 to 20
for idx, (loan_type, params) in enumerate(loan_details.items(), start=1):
    product = {
        'loan_product_id': idx,
        'loan_type': loan_type,
        'purchase_category': loan_type_to_category.get(loan_type, None),
        'min_interest_rate': params['interest_range'][0],
        'max_interest_rate': params['interest_range'][1],
        'min_term_months': params['term_range'][0],
        'max_term_months': params['term_range'][1],
        'min_loan_amount': params['loan_amount_range'][0],
        'max_loan_amount': params['loan_amount_range'][1],
        'processing_fee': np.round(np.random.uniform(100, 1000), 2)
    }
    loan_product_data.append(product)

df_loan_products = pd.DataFrame(loan_product_data)
df_loan_products.to_csv('loan_product_data.csv', index=False)
print("Loan product details dataset created: loan_product_data.csv")

# --- 2. Create Historical Loan Application Records ---
# Assume you have a customers dataset with a column 'cid'
num_customers = args.num_customers  # Adjust as needed
customer_ids = np.arange(1, num_customers + 1)

# Generate synthetic historical loan applications
num_applications = args.num_applications  # Number of historical loan applications
# Generate customer data
customers = pd.DataFrame({
    'customer_id': np.arange(1, args.num_customers + 1),
    'age': np.random.randint(21, 70, args.num_customers),
    'annual_income': np.random.normal(50000, 20000, args.num_customers).astype(int),  # Normal distribution around 50k
    'credit_score': np.clip(np.random.normal(680, 50, args.num_customers), 300, 850).astype(int)  # Normal dist, clipped to valid range
})

# Generate loan applications with the required structure
def generate_loan_application(application_id):
    customer = customers.sample(1).iloc[0]
    product = df_loan_products.sample(1).iloc[0]  # Randomly select loan product
    
    loan_amount = np.random.randint(product['min_loan_amount'], product['max_loan_amount'])
    term = np.random.randint(product['min_term_months'], product['max_term_months'])
    interest_rate = round(np.random.uniform(product['min_interest_rate'], product['max_interest_rate']), 2)
    credit_score = customer['credit_score']
    income = customer['annual_income']
    debt_to_income = round(np.random.uniform(0.1, 0.6), 2)  # Random DTI ratio between 10% and 60%
    application_date = datetime.today() - timedelta(days=np.random.randint(0, 365 * 3))  # Within last 3 years
    
    # More realistic approval logic
    approval_prob = 0.5  # Base probability
    
    if credit_score > 750:
        approval_prob += 0.3
    elif credit_score < 600:
        approval_prob -= 0.3
    
    if income > 70000:
        approval_prob += 0.2
    elif income < 30000:
        approval_prob -= 0.2
    
    if product['loan_type'] == 'home' and credit_score < 650:
        approval_prob -= 0.2  # Stricter approval criteria for home loans
    
    status = 'approved' if np.random.rand() < approval_prob else 'rejected'
    
    return {
        'application_id': application_id,
        'cid': customer['customer_id'],
        'loan_product_id': product['loan_product_id'],
        'loan_amount': loan_amount,
        'interest_rate': interest_rate,
        'loan_term_months': term,
        'credit_score': credit_score,
        'annual_income': income,
        'debt_to_income_ratio': debt_to_income,
        'application_date': application_date.strftime("%Y-%m-%d"),
        'status': status
    }

loan_applications = pd.DataFrame([generate_loan_application(i + 1) for i in range(args.num_applications)])

# Save dataset
loan_applications.to_csv('loan_applications.csv', index=False)
print("Dataset generated successfully!")
