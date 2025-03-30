import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import MyFin from '../../src/components/MyFin';
import { getSpendsChartData } from '../../src/api/spends';
import { getLoanRecommendations } from '../../src/api/financial_products';
import { User, UserType } from '../../src/types/auth';
import { SpendData } from '../../src/types/spend';
import { Loan } from '../../src/types/financial_product';
import React from "react";

vi.mock('../../src/api/spends');
vi.mock('../../src/api/financial_products');
vi.mock('../../src/components/PieChartDisplay', () => ({
    default: () => <div>PieChartDisplay</div>
}))

const mockUser: User = { id: 1, type: UserType.Customer, username: "testuser" };
const mockSpendData: SpendData = {
    category: [{ category: 'Food', spend: 200 }],
    payment_mode: [{ mode: 'Credit Card', spend: 150 }]
};
const mockLoanRecs: Loan[] = [
    {
      "loan_product_id": 18,
      "approval_probability": 0.7823603749275208,
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
      "approval_probability": 0.6812320351600647,
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
    }
  ]

describe('MyFin Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders without crashing', () => {
        vi.mocked(getLoanRecommendations).mockImplementation(async () => new Response(JSON.stringify(mockLoanRecs)));
        vi.mocked(getSpendsChartData).mockImplementation(async () => new Response(JSON.stringify(mockSpendData)));
        
        render(<MyFin user={mockUser} />);
        expect(screen.getByText('MyFin: My Financials')).toBeInTheDocument();
    });

    it('fetches and displays spend data', async () => {
        vi.mocked(getSpendsChartData).mockImplementation(async () => new Response(JSON.stringify(mockSpendData)));
        vi.mocked(getLoanRecommendations).mockImplementation(async () => new Response(JSON.stringify(mockLoanRecs)));

        render(<MyFin user={mockUser} />);

        await waitFor(() => {
            expect(screen.getByText('PieChartDisplay')).toBeInTheDocument();
        });
    });

    it('fetches and displays loan recommendations', async () => {
        vi.mocked(getLoanRecommendations).mockImplementation(async () => new Response(JSON.stringify(mockLoanRecs)));
        vi.mocked(getSpendsChartData).mockImplementation(async () => new Response(JSON.stringify(mockSpendData)));

        render(<MyFin user={mockUser} />);

        await waitFor(() => {
            expect(screen.getByText('Loan Recommendations')).toBeInTheDocument();
            expect(screen.getByText('Eco Friendly Loan')).toBeInTheDocument();
        });
    });

    it('does not fetch data if user is null', () => {
        render(<MyFin user={null} />);
        expect(getSpendsChartData).not.toHaveBeenCalled();
        expect(getLoanRecommendations).not.toHaveBeenCalled();
    });
});