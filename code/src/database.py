import sqlite3
import pandas as pd
from models import UserType

import datetime

conn = sqlite3.connect('database.db')
c = conn.cursor()

def init_connection():
    """initiate a new connection with the database
    """

    global conn, c
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

def drop_existing_tables():
    """drop the existing tables in the database
    """

    c.execute('drop table if exists transactions')
    c.execute('drop table if exists loan_applications')
    c.execute('drop table if exists products')
    c.execute('drop table if exists businesses')
    c.execute('drop table if exists customers')
    c.execute('drop table if exists social_media')
    c.execute('drop table if exists loan_products')
    conn.commit()
    print('Tables dropped')

def init_customers():
    """Create the customers table
    """

    c.execute('''
    create table if not exists customers (
    cid integer primary key autoincrement,
    name text,
    age integer,
    gender text,
    location text,
    annual_income integer,
    education text,
    occupation text
    )''')
    
    customers_df = pd.read_csv('initial_data/customers_usa.csv')
    for (_, row) in customers_df.iterrows():
        c.execute('''
        insert into customers (name, age, gender, location, annual_income, education, occupation)
        values (?, ?, ?, ?, ?, ?, ?)''',
        (row['name'], row['age'], row['gender'], row['location'], row['annual_income'], row['education'], row['occupation']))
    
    conn.commit()
    print('Customers initialized')

def init_businesses():
    """Create the businesses table
    """

    c.execute('''
    create table if not exists businesses (
    bid integer primary key autoincrement,
    category text,
    business_name text,
    revenue real,
    num_employees integer
    )''')
    
    businesses_df = pd.read_csv('initial_data/business_data.csv')
    for (_, row) in businesses_df.iterrows():
        c.execute('''
        insert into businesses (category, business_name, revenue, num_employees)
        values (?, ?, ?, ?)''',
        (row['category'], row['business_name'], row['revenue'], row['num_employees']))
    
    conn.commit()
    print('Businesses initialized')

def init_products():
    """Create the products table
    """

    c.execute('''
    create table if not exists products (
    pid integer primary key autoincrement,
    bid integer,
    product_name text,
    popularity real,
    price real,
    geo_demand text,
    foreign key (bid) references businesses(bid)
    )''')

    products_df = pd.read_csv('initial_data/product_data.csv')
    for (_, row) in products_df.iterrows():
        c.execute('''
        insert into products (bid, product_name, popularity, price, geo_demand)
        values (?, ?, ?, ?, ?)''',
        (row['bid'], row['product_name'], row['popularity'], row['price'], row['geo_demand']))
    
    conn.commit()
    print('Products initialized')

def init_transactions():
    """Create the transactions table
    """

    c.execute('''
    create table if not exists transactions (
    tid integer primary key autoincrement,
    cid integer,
    pid integer,
    amount real,
    purchase_date timestamp,
    payment_mode text,
    foreign key (cid) references customers(cid),
    foreign key (pid) references products(pid)
    )''')

    transactions_df = pd.read_csv('initial_data/transactions.csv')
    for (_, row) in transactions_df.iterrows():
        c.execute('''
        insert into transactions (cid, pid, amount, purchase_date, payment_mode)
        values (?, ?, ?, ?, ?)''',
        (row['cid'], row['pid'], row['amount'], row['purchase_date'], row['payment_mode']))
    
    conn.commit()
    print('Transactions initialized')

def init_social_media():
    """Create the social media table
    """

    c.execute('''
    create table if not exists social_media (
    post_ID integer primary key autoincrement,
    platform text,
    content text,
    timestamp timestamp,
    sentiment_score real,
    category text)''')

    social_media_df = pd.read_csv('initial_data/social_media_posts.csv')
    for (_, row) in social_media_df.iterrows():
        c.execute('''
        insert into social_media (platform, content, timestamp, sentiment_score, category)
        values (?, ?, ?, ?, ?)''',
        (row['platform'], row['content'], row['timestamp'], row['sentiment_score'], row['category']))
    
    conn.commit()
    print('Social media initialized')

def init_loan_products():
    """Create the loan_products table
    """

    c.execute('''
    create table if not exists loan_products (
        loan_product_id INTEGER PRIMARY KEY autoincrement,
        loan_type TEXT,
        purchase_category TEXT,
        min_interest_rate REAL,
        max_interest_rate REAL,
        min_term_months INTEGER,
        max_term_months INTEGER,
        min_loan_amount INTEGER,
        max_loan_amount INTEGER,
        processing_fee REAL
    )''')
    
    loan_products_df = pd.read_csv('initial_data/loan_product_data.csv')
    for (_, row) in loan_products_df.iterrows():
        c.execute('''
        insert into loan_products (loan_product_id, loan_type, purchase_category, min_interest_rate, max_interest_rate, min_term_months, max_term_months, min_loan_amount, max_loan_amount, processing_fee)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (row['loan_product_id'], row['loan_type'], row['purchase_category'], row['min_interest_rate'], row['max_interest_rate'], row['min_term_months'], row['max_term_months'], row['min_loan_amount'], row['max_loan_amount'], row['processing_fee']))
    
    conn.commit()
    print('Loan products initialized')

def init_loan_applications():
    """Create the loan applications table
    """

    c.execute('''
    create table if not exists loan_applications (
    application_id integer primary key autoincrement,
    cid integer,
    loan_product_id integer,
    loan_amount real,
    interest_rate real,
    loan_term_months integer,
    credit_score integer,
    annual_income real,
    debt_to_income_ratio real,
    application_date date,
    status text,
    foreign key (cid) references customers(cid)
    foreign key (loan_product_id) references loan_products(loan_product_id)
    )''')
    
    loan_applications_df = pd.read_csv('initial_data/loan_applications.csv')
    for (_, row) in loan_applications_df.iterrows():
        c.execute('''
        insert into loan_applications (application_id, cid, loan_product_id, loan_amount, interest_rate, 
                                       loan_term_months, credit_score, annual_income, debt_to_income_ratio, 
                                       application_date, status)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (row['application_id'], row['cid'], row['loan_product_id'], row['loan_amount'], row['interest_rate'],
         row['loan_term_months'], row['credit_score'], row['annual_income'], row['debt_to_income_ratio'],
         row['application_date'], row['status']))
    
    conn.commit()
    print('Loan applications initialized')

def init_db():
    """
    Drops (if existing) and re-initializes all the tables in the database
    """

    c.execute('pragma foreign_keys=on')
    drop_existing_tables()
    init_customers()
    init_businesses()
    init_products()
    init_transactions()
    init_social_media()
    init_loan_products()
    init_loan_applications()
    print("initialization complete")

def close_connection():
    """Close the connection
    """

    conn.close()
    c = None
    print('Connection closed')

def get_first_n(table_name, n):
    """Get the first n records from a table
    
    Keyword arguments:
    table_name -- Name of the table to query
    n -- Number of rows needed
    Return: List of tuples with required number of rows
    """

    c.execute(f'select * from {table_name} limit {n}')
    rows = c.fetchall()
    return rows

def get_df_from_table(table_name, limit=None, order_by=None, order=None, index_col=None):
    """Get a subsection (or full table) from a table as a DataFrame
    
    Keyword arguments:
    table_name -- Name of the table to query
    limit -- Number of rows to query (default: all)
    order_by -- Column name to order by (default: None)
    order -- 'ASC' or 'DESC' (case-insensitive) (mandatory when order_by is given)
    index_col -- Column name to make the index of the DataFrame (default: None)

    Return: DataFrame
    """
    
    if not c:
        init_connection()

    query = f'select * from {table_name}'
    if order_by:
        query += f' order by {order_by}'
        if order:
            query += f' {order}'
    if limit:
        query += f' limit {limit}'
    
    return pd.read_sql_query(query, conn, index_col=index_col)

def execute_and_fetch_rows(query, as_df=False, index_col=None):
    """Executes a query and fetches all the rows, optionally as a DataFrame
    
    Keyword arguments:
    query -- string, what to execute
    as_df -- boolean, returns a DataFrame if True, otherwise a List of Tuples (default: False)
    index_col -- string, the column to make the index of the dataframe (default: None)
    Return: List of tuples or DataFrame
    """

    if not c:
        init_connection()
    
    result = c.execute(query).fetchall()
    if as_df:
        df = pd.DataFrame(result, columns=[desc[0] for desc in c.description])
        if index_col:
            df.set_index(index_col, inplace=True)
        return df
    return result
    
def execute_and_fetch_one(query, as_df=False):
    """Executes a query and fetches the first row, optionally as a DataFrame
    
    Keyword arguments:
    query -- string, what to execute
    as_df -- boolean, returns a DataFrame if True, otherwise a List of Tuples (default: False)
    Return: List of tuples or DataFrame
    """

    if not c:
        init_connection()
    
    result = c.execute(query).fetchone()
    if as_df:
        return pd.DataFrame([result], columns=[desc[0] for desc in c.description]) if result else pd.DataFrame()
    return result

def get_last_n_transactions_for_customer(cid:int, n:int=10, as_df = False):
    """Get the last {n} transactions for the customer
    
    Keyword arguments:
    cid -- id of the customer
    n -- number of transactions (default: 10)
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """
    
    query = f'''
    select tid, pid, amount, purchase_date, payment_mode
    from transactions
    where cid = {cid}
    order by purchase_date desc
    limit {n}
    '''
    return execute_and_fetch_rows(query, as_df=as_df)

def get_last_n_transactions_for_all_customers(n:int=10, as_df=False):
    """Get the last {n} transactions for all the customers as a batch query
    
    Keyword arguments:
    n -- number of transactions (default: 10)
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """

    query = f'''
    select tid, cid, pid, amount, purchase_date, payment_mode
    from (
        select 
            tid, cid, pid, amount, purchase_date, payment_mode,
            ROW_NUMBER() over (partition by cid order by purchase_date DESC) AS rn
        from transactions
    )
    where rn <= {n}
    '''
    result = execute_and_fetch_rows(query, as_df=as_df)
    if as_df:
        # make it a dictionary of dataframes for each cid
        result_grouped = {}
        for cid, df in result.groupby('cid'):
            result_grouped[cid] = df
        return result_grouped
    return result

def get_last_n_social_media_posts(n:int, as_df=False):
    """Get last {n} social media posts from the database
    
    Keyword arguments:
    n -- number of posts
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """
    
    query = f'''
    select * from social_media order by timestamp desc limit {n}
    '''
    return execute_and_fetch_rows(query, as_df=as_df)

def get_avg_recent_sentiment(n:int=None, as_df=False):
    """Calculates the average sentiment for each category based on the last {n} social media posts
    
    Keyword arguments:
    n -- number of posts (default: all)
    as_df -- whether to convert it into a DataFrame

    Return: DataFrame or List of Tuples
    """
    
    subquery = "select * from social_media order by timestamp desc"
    if n:
        subquery += f' limit {n}'
    
    query = f'''
    select category, avg(sentiment_score) as avg_sentiment
    from (
        {subquery}
    )
    group by category
    '''
    return execute_and_fetch_rows(query, as_df=as_df, index_col='category' if as_df else None)

def get_product_by_pid(pid:int, as_df=False):
    """Return the product and business information based on pid
    
    Keyword arguments:
    pid -- id of the product
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """
    
    query = f'''
    select p.*, b.category 
    from products p join businesses b
    on p.bid = b.bid
    where p.pid = {pid}
    '''
    return execute_and_fetch_one(query, as_df=as_df)

def search_products_by_name(query: str, as_df=False):
    search_query = f"""
    SELECT p.*, b.category, b.business_name
    FROM products p
    JOIN businesses b ON p.bid = b.bid
    WHERE p.product_name LIKE '%{query}%'
    """
    return execute_and_fetch_rows(search_query, as_df)

def get_customer_by_cid(cid:int, as_df=False):
    """Return the customer based on cid
    
    Keyword arguments:
    cid -- id of the customer
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """

    query = f'''
    select * from customers where cid = {cid}
    '''
    return execute_and_fetch_one(query, as_df=as_df)

def get_business_by_bid(bid:int, as_df=False):
    """Return the business based on bid
    
    Keyword arguments:
    bid -- id of the business
    as_df -- whether to convert it into a DataFrame
    
    Return: List of Tuples or DataFrame
    """

    query = f'''
    select * from businesses where bid = {bid}
    '''
    return execute_and_fetch_one(query, as_df=as_df)

def get_last_n_loan_applications_by_cid(cid:int, n:int=None, as_df=False):
    """Return the loan applications for a customer
    
    Keyword arguments:
    cid -- id of the customer
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """

    query = f'''
    select * from loan_applications where cid = {cid} order by application_date desc
    '''

    if n:
        query += f""" limit {n}
        """
    return execute_and_fetch_rows(query, as_df=as_df)

def validate_user(user_id:str, password:str, user_type:UserType) -> pd.DataFrame:
    """Validate user credentials and type
    
    Keyword arguments:
    user_id -- id of the customer or business
    password -- password

    Return: boolean indicating status of authentication  
    """

    if password != 'password':
        return None
    if user_type == UserType.CUSTOMER:
        result = get_customer_by_cid(user_id, as_df=True)
    elif user_type == UserType.BUSINESS:
        result = get_business_by_bid(user_id, as_df=True)
    else:
        return None
    return result.iloc[0].to_dict() if not result.empty else None

# init_db() 


def get_category_and_payment_summary(cid: int, after_date: datetime.date = None):
    """Get aggregated spend by category and payment mode for a given customer.

    Keyword arguments:
    cid -- id of the customer

    Return: JSON-like dictionary
    """

    where_clause = f"WHERE t.cid = {cid}"
    if after_date:
        after_date_str = after_date.strftime('%Y-%m-%d %H:%M:%S')
        where_clause += f" AND t.purchase_date >= '{after_date_str}'"

    # Query to aggregate spend by category
    category_query = f'''
    SELECT b.category, SUM(t.amount) as spend
    FROM transactions t
    JOIN products p ON t.pid = p.pid
    JOIN businesses b ON p.bid = b.bid
    {where_clause}
    GROUP BY b.category
    '''

    print(category_query)

    # Query to aggregate spend by payment mode
    payment_query = f'''
    SELECT t.payment_mode as mode, SUM(t.amount) as spend
    FROM transactions t
    {where_clause}
    GROUP BY t.payment_mode
    '''

    # Execute both queries and fetch results
    category_data = execute_and_fetch_rows(category_query)
    payment_data = execute_and_fetch_rows(payment_query)

    # Format category data
    category_summary = [{"category": row[0], "spend": row[1]} for row in category_data]
    
    # Format payment mode data
    payment_summary = [{"mode": row[0], "spend": row[1]} for row in payment_data]

    # Combine the results
    result = {
        "category": category_summary,
        "payment_mode": payment_summary
    }
    print(result)

    return result


def get_product_revenue_info(bid: int, as_df=False):
    """Get aggregated revenue by product for a given business.

    Keyword arguments:
    bid -- id of the business
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """

    # Query to aggregate revenue by product
    product_query = f'''
    SELECT p.product_name, SUM(t.amount) as spend
    FROM transactions t
    JOIN products p ON t.pid = p.pid
    WHERE p.bid = {bid}
    GROUP BY t.pid
    '''

    # Execute query and fetch results
    result = execute_and_fetch_rows(product_query, as_df=as_df)

    return result

def get_payment_mode_revenue_info(bid: int, as_df=False):
    """Get aggregated revenue by payment mode for a given business.

    Keyword arguments:
    bid -- id of the business
    as_df -- whether to convert it into a DataFrame

    Return: List of Tuples or DataFrame
    """

    # Query to aggregate revenue by payment_mode
    payment_mode_query = f'''
    SELECT t.payment_mode, SUM(t.amount) as spend
    FROM transactions t
    JOIN products p ON t.pid = p.pid
    WHERE p.bid = {bid}
    GROUP BY t.payment_mode
    '''

    # Execute query and fetch results
    result = execute_and_fetch_rows(payment_mode_query, as_df=as_df)

    return result


if __name__ == '__main__':
    init_db()
    close_connection()

