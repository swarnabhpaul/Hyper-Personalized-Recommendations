import pandas as pd
import argparse
from transformers import pipeline
from llm_chat import prompt_model
from database import get_df_from_table

gender_map = {
    'm': "Male",
    'f': "Female",
    'o': "Other",
}

education_map = {
    "d": "diploma",
    "b": "bachelor",
    "m": "master",
    "p": "phd",
}

def generate_insights(bid):
    business_df = get_df_from_table("businesses")
    my_business = business_df[business_df["bid"] == bid].iloc[0]
    product_df = get_df_from_table("products")
    product_df = product_df[product_df["bid"] == bid]
    social_media_df = get_df_from_table("social_media")
    social_media_df = social_media_df[social_media_df["category"] == my_business.category]["sentiment_score"].mean()

    social_context = f"The average sentiment score on social media for the category in which this business operates is {social_media_df:.2f}."
    business_context = business_df[business_df["bid"] == bid].to_string(index=False)
    product_context = product_df.to_string(index=False)

    customer_df = get_df_from_table("customers")
    my_product_ids = product_df["pid"].tolist()

    transactions_df = get_df_from_table("transactions")
    transactions_df = transactions_df[transactions_df["pid"].isin(my_product_ids)]

    customer_spend = transactions_df.groupby("cid")["amount"].sum().reset_index()
    customer_spend = customer_spend.sort_values("amount", ascending=False)

    total_customers = customer_spend.shape[0]

    top_customers = customer_spend[:int(0.05*total_customers)+1]

    top_customers = top_customers.merge(customer_df, on="cid", how="left")

    age_mean = top_customers["age"].mean()
    gender_mode = top_customers["gender"].mode()[0]
    annual_income_mean = top_customers["annual_income"].mean()
    annual_income_min, annual_income_max = top_customers["annual_income"].min(), top_customers["annual_income"].max()
    education_mode = top_customers["education"].mode()[0]

    customers_context = f'''The top 5% of customers for this business have the following characteristics:
    - Average age: {age_mean:.2f}
    - Most common gender: {gender_map[gender_mode]}
    - Average annual income: ${annual_income_mean:.2f}
    - Range of annual income: ${annual_income_min:.2f} to ${annual_income_max:.2f}
    - Most common education level: {education_map[education_mode]}
    '''
    
    # Build an aggregated context with limited column samples
    aggregated_context = (
        "Business Data:\n" + business_context + "\n\n" +
        "Customer Data:\n" + customers_context + "\n\n" +
        "Product Data:\n" + product_context + "\n\n" +
        # "Transaction Data:\n" + transactions_context + "\n\n" +
        "Social Media Data:\n" + social_context + "\n\n" + 
        "Notes: All revenues and prices are in USD. For the product data, the popularity score is a measure of how well the product is selling, and it ranges from 0 to 10. Social media sentiment score is between -1 and 1 where -1 indicates negative sentiment and 1 indicates positive sentiment."
    )

    # Construct the prompt with aggregated context and instructions
    prompt = (
        "You are an AI financial advisor for businesses. Using the aggregated data context below, "
        "generate 3 one-sentence actionable items for the business and 3 one-sentence follow-up questions that the business might ask next. \n"
        "Output format:\n"
        "Line 1: Action item 1\n"
        "Line 2: Action item 2\n"
        "Line 3: Action item 3\n"
        "Line 4: (empty)\n"
        "Line 5: Question 1\n"
        "Line 6: Question 2\n"
        "Line 7: Question 3\n"
        "Do not include any extra text. No need to label the lines as item 1,2, etc.\n\n"
        "Aggregated Data Context:\n" + aggregated_context
    )

    # Use a free model that is more capable, comparable to ChatGPT-style performance:
    # "google/flan-ul2" is one of the most advanced free instruction-following models.
    
    generation_status, result = prompt_model(prompt)
    return generation_status, result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AI-powered financial advisor insights using aggregated context from multiple datasets."
    )
    parser.add_argument("--bid", type=int, required=True, help="Business ID")
    args = parser.parse_args()
    
    print(generate_insights(args.bid))
