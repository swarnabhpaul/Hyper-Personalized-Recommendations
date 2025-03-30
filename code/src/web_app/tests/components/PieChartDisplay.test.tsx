import {describe, it, expect, vi, beforeEach} from "vitest";
import { render , screen } from '@testing-library/react';
import PieChartDisplay from '../../src/components/PieChartDisplay';
import { PieData } from '../../src/types/charts';
import React from "react";

vi.mock('../../src/components/PieChart', () => ({default: () => <div>PieChart</div>}));

describe('PieChartDisplay', () => {
    const pieData1: PieData[] = [
        { name: 'Category 1', value: 100, color: '#FF0000' },
        { name: 'Category 2', value: 200, color: '#00FF00' },
    ];

    const pieData2: PieData[] = [
        { name: 'Category A', value: 150, color: '#0000FF' },
        { name: 'Category B', value: 250, color: '#FFFF00' },
    ];

    beforeEach(() => {
        global.ResizeObserver = vi.fn().mockReturnValue({
            observe: vi.fn(),
            unobserve: vi.fn(),
            disconnect: vi.fn(),
        });
    });

    it('renders heading', () => {
        render(<PieChartDisplay heading="Test Heading" />);
        expect(screen.getByText('Test Heading')).toBeInTheDocument();
    });

    it('renders description if provided', () => {
        render(<PieChartDisplay heading="Test Heading" description="Test Description" />);
        expect(screen.getByText('Test Description')).toBeInTheDocument();
    });

    it('does not render description if not provided', () => {
        const { queryByText } = render(<PieChartDisplay heading="Test Heading" />);
        expect(queryByText('Test Description')).not.toBeInTheDocument();
    });

    it('renders PieChart component if pieData1 is provided', () => {
        render(<PieChartDisplay heading="Test Heading" pieData1={pieData1} />);
        const pieCharts = screen.getAllByText('PieChart');
        expect(pieCharts).toHaveLength(1);
    });

    it('renders PieChart component if pieData2 is provided', () => {
        render(<PieChartDisplay heading="Test Heading" pieData2={pieData2} />);
        const pieCharts = screen.getAllByText('PieChart');
        expect(pieCharts).toHaveLength(1);
    });

    it('renders two PieChart components if both pieData1 and pieData2 are provided', () => {
        render(<PieChartDisplay heading="Test Heading" pieData1={pieData1} pieData2={pieData2} />);
        const pieCharts = screen.getAllByText('PieChart');
        expect(pieCharts).toHaveLength(2);
    });
});