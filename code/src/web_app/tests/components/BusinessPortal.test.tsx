import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import { describe, it, vi, expect } from 'vitest';
import BusinessPortal from '../../src/components/BusinessPortal';
import { getBusinessKPI } from '../../src/api/kpi';
import { getBusinessInsights } from '../../src/api/business_insights';
import { User, UserType } from '../../src/types/auth';

vi.mock('../../src/api/kpi');
vi.mock('../../src/api/business_insights');
vi.mock('../../src/components/PieChartDisplay', () => ({
    default: () => <div>PieChartDisplay</div>
}))

const mockUser: User = { id: 1, username: "testuser", type: UserType.Business};
const mockKPIData = {
    products: [
        { product_name: 'Product 1', amount: 100 },
        { product_name: 'Product 2', amount: 200 },
    ],
    payment_mode: [
        { mode: 'Credit Card', amount: 150 },
        { mode: 'Cash', amount: 150 },
    ],
};
const mockInsights = {
    action_items: ['Increase marketing budget', 'Expand to new markets'],
    questions: ['What are our biggest challenges?', 'How can we improve customer satisfaction?'],
};


describe('BusinessPortal', () => {
    it('renders without crashing', async () => {
        vi.mocked(getBusinessKPI).mockImplementation(async () => new Response(JSON.stringify(mockKPIData)));
        vi.mocked(getBusinessInsights).mockImplementation(async () => new Response(JSON.stringify(mockInsights)));

        await act(async () => {
            render(<BusinessPortal user={mockUser} />);
        });
        expect(screen.getByText('PieChartDisplay')).toBeInTheDocument();
    });

    it('fetches and displays KPI data', async () => {

        vi.mocked(getBusinessKPI).mockImplementation(async () => new Response(JSON.stringify(mockKPIData)));
        vi.mocked(getBusinessInsights).mockImplementation(async () => new Response(JSON.stringify(mockInsights)));

        await act(async () => {
            render(<BusinessPortal user={mockUser} />);
        });

        expect(screen.getByText('PieChartDisplay')).toBeInTheDocument();
    });

    it('fetches and displays business insights', async () => {
        
        vi.mocked(getBusinessInsights).mockImplementation(async () => new Response(JSON.stringify(mockInsights)));
        vi.mocked(getBusinessKPI).mockImplementation(async () => new Response(JSON.stringify(mockKPIData)));

        await act(async () => {
            render(<BusinessPortal user={mockUser} />);
        });

        await waitFor(() => {
            expect(screen.getByText(/Increase marketing budget/)).toBeInTheDocument();
            expect(screen.getByText(/Expand to new markets/)).toBeInTheDocument();
            expect(screen.getByText(/What are our biggest challenges?/)).toBeInTheDocument();
            expect(screen.getByText(/How can we improve customer satisfaction?/)).toBeInTheDocument();
        });
        });

        it('displays an error message when fetching insights fails', async () => {
        vi.mocked(getBusinessInsights).mockImplementation(async () => new Response(JSON.stringify({ detail: 'Error fetching insights' }), { status: 500 }));

        await act(async () => {
            render(<BusinessPortal user={mockUser} />);
        });

        await waitFor(() => {
            expect(screen.getByText(/Error fetching insights/)).toBeInTheDocument();
        });
    });
});