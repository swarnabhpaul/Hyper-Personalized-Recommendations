import pandas as pd
import random
from faker import Faker
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Generate fake customer profiles.')
parser.add_argument('--filename', type=str, default='customers.csv', help='Output CSV file name')
parser.add_argument('--start_id', type=int, default=1, help='Starting customer ID')
parser.add_argument('--num_customers', type=int, default=10000, help='Number of customer profiles to generate')

args = parser.parse_args()

fake = Faker()

start_id = args.start_id

# Generate customer profiles
num_customers = args.num_customers
income_ranges = [[20000, 40000], [40001, 70000], [70001, 100000], [100001, 150000], [150001, 250000], [250001, 1000000]]
income_probability = [0.2, 0.3, 0.25, 0.15, 0.08, 0.02]
customers = []
genders = ["m", "f", "o"]
educations = ["b", "m", "p", "d"]
for i in range(start_id, num_customers + start_id):
    gender = random.choice(genders)
    income_range = random.choices(income_ranges, weights=income_probability)[0]
    customers.append([
        i,
        fake.name_male() if gender == "m" else fake.name_female() if gender == "f" else fake.name_nonbinary(),
        random.randrange(18,76),
        gender,
        fake.city(),
        random.randint(income_range[0], income_range[1]),
        random.choice(educations),
        fake.job(),
    ])

customer_df = pd.DataFrame(customers, columns=["cid", "name", "age", "gender", "location", "annual_income", "education", "occupation"])

# Save to CSV
customer_file = args.filename

if start_id == 1:
    customer_df.to_csv('customers_usa.csv', index=False)
else:
    customer_df.to_csv('customers_usa.csv', mode='a', header=False, index=False)

customer_df.to_csv(customer_file, index=False)
print(f"Customer profiles saved to {customer_file}")
