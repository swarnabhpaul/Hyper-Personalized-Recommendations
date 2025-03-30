import pandas as pd
from faker import Faker
import random
import argparse

parser = argparse.ArgumentParser(description='Generate fake transaction data.')
parser.add_argument('--start_id', type=int, default=1, help='Starting transaction ID')
parser.add_argument('--num_records', type=int, default=100000, help='Number of transactions to generate')
parser.add_argument('--num_customers', type=int, default=10000, help='Number of customers')

args = parser.parse_args()

# Initialize Faker
fake = Faker()

# Define the parameters
num_records = args.num_records  # Number of transactions
start_id = args.start_id  # Starting transaction ID
num_customers = args.num_customers  # Number of customers

# Define payment modes
payment_modes = ['Credit', 'Debit', 'Net Banking', 'Wire Transfer']

# Load the CSV file
df_products = pd.read_csv('product_data.csv')

# Extract the 'Price' column into a list
pid_prices = df_products['price'].tolist()

# Print the list to verify (Optional)
print("✅ Price list loaded:", pid_prices[:10])  # Print first 10 prices to verify

# Generate transaction data
data = []
for tid in range(start_id, num_records + start_id):
    pid = random.randint(1, 30)  # Product ID between 1 and 30

    # Check if the price is available for the selected Pid
    if pid <= len(pid_prices):
        base_price = pid_prices[pid - 1]  # Get the price for the product (index is pid - 1)
        
        # Calculate a random amount between 20% less and 20% more
        variation_percent = random.uniform(-0.2, 0.2)  # -20% to +20%
        amount = round(base_price * (1 + variation_percent), 2)
    else:
        # Fallback in case Pid is out of bounds (optional)
        amount = round(random.uniform(10, 10000), 2)

    record = {
        'tid': tid,                                          # Transaction ID (1-10000)
        'cid': random.randint(1, num_customers),                      # Customer ID (1-1000)
        'pid': pid,                                          # Product ID (1-30)
        'amount': amount*random.randint(1,4),                                    # Adjusted Amount
        'purchase_date': fake.date_time_this_year(),         # Timestamp within this year
        'payment_mode': random.choice(payment_modes)         # Random payment mode
    }
    data.append(record)

# Create a DataFrame using pandas
df_transactions = pd.DataFrame(data)

# Print sample data for verification
print(df_transactions.head())

# Write to CSV file

if start_id == 1:
    df_transactions.to_csv('transactions.csv', index=False)
else:
    df_transactions.to_csv('transactions.csv', mode='a', header=False, index=False)

print("✅ CSV file 'transactions.csv' generated successfully!")