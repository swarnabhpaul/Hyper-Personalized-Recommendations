import { act, render, screen } from "@testing-library/react"
import { describe, it, expect, beforeEach, vi } from "vitest"
import PieChart from "../../src/components/PieChart"
import { PieData } from "../../src/types/charts"
import React from "react";

const mockPieData: PieData[] = [
    { name: "Category A", value: 400, color: "#0088FE" },
    { name: "Category B", value: 300, color: "#00C49F" },
    { name: "Category C", value: 300, color: "#FFBB28" },
    { name: "Category D", value: 200, color: "#FF8042" },
]

vi.mock('recharts', async () => {
    const originalModule = await vi.importActual('recharts');
    return {
        ...originalModule,
        ResponsiveContainer: ({ children }) => <div>Responsive Container {children}</div>,
        PieChart: ({children}) => <div>PieChart {children}</div>,
        Pie: ({children}) => <div>Pie {children}</div>,
        Cell: ({children}) => <div>Cell {children}</div>
    };
});

describe("PieChart Component", () => {

    beforeEach(() => {
        global.ResizeObserver = vi.fn().mockReturnValue({
            observe: vi.fn(),
            unobserve: vi.fn(),
            disconnect: vi.fn(),
        });
    });

    it("renders without crashing", async () => {
        await act(async () => {
            render(<PieChart pieData={mockPieData} />)
        });
        expect(screen.getByText('PieChart')).toBeInTheDocument();
    });

    it('renders the correct number of cells', async () => {
        await act(async () => {
            render(<PieChart pieData={mockPieData} />)
        });
        expect(screen.getAllByText('Cell')).toHaveLength(mockPieData.length);
    })
})