export interface Loan {
    loan_product_id: number;
    loan_type: string;
    approval_probability: number;
    purchase_category: string;
    min_interest_rate: number;
    max_interest_rate: number;
    min_loan_amount: number;
    max_loan_amount: number;
    min_term_months: number;
    max_term_months: number;
    processing_fee: number;
    loan_type_readable: string;
}