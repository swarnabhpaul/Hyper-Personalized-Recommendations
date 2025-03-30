import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ProductHub from "../../src/components/ProductHub";
import { getRecommended, searchProducts } from "../../src/api/products";
import { User, UserType } from "../../src/types/auth";
import { Product } from "../../src/types/product";
import React from "react";

vi.mock("../../src/api/products");

describe("ProductHub", () => {
    const mockUser: User = { id: 1, username: "testuser", type: UserType.Customer};
    const mockProducts: Product[] = [
        { id: 1, product_name: "Product 1", business_name: "Business 1" },
        { id: 2, product_name: "Product 2", business_name: "Business 2" },
    ];

    it("renders recommended products when user is provided", async () => {
        vi.mocked(getRecommended).mockImplementation(async () => new Response(JSON.stringify(mockProducts)));

        render(<ProductHub user={mockUser} />);

        expect(await screen.findByText("Recommended Products")).toBeInTheDocument();
        expect(await screen.findByText("Product 1")).toBeInTheDocument();
        expect(await screen.findByText("Product 2")).toBeInTheDocument();
    });

    it("renders search results when a search is performed", async () => {
        vi.mocked(searchProducts).mockImplementation(async () => new Response(JSON.stringify(mockProducts)));

        render(<ProductHub user={mockUser} />);

        const searchInput = screen.getByPlaceholderText("Search for products");
        const searchButton = screen.getByText("Search");

        fireEvent.change(searchInput, { target: { value: "Test" } });
        fireEvent.click(searchButton);

        expect(await screen.findByText('Search Results for "Test"')).toBeInTheDocument();
        expect(await screen.findByText("Product 1")).toBeInTheDocument();
        expect(await screen.findByText("Product 2")).toBeInTheDocument();
    });

    it("resets search results when reset button is clicked", async () => {
        vi.mocked(searchProducts).mockImplementation(async () => new Response(JSON.stringify(mockProducts)));

        render(<ProductHub user={mockUser} />);

        const searchInput = screen.getByPlaceholderText("Search for products");
        const searchButton = screen.getByText("Search");
        const resetButton = screen.getByText("Reset");

        fireEvent.change(searchInput, { target: { value: "Test" } });
        fireEvent.click(searchButton);

        expect(await screen.findByText('Search Results for "Test"')).toBeInTheDocument();

        fireEvent.click(resetButton);

        expect(screen.queryByText('Search Results for "Test"')).not.toBeInTheDocument();
        expect(screen.getByText("Recommended Products")).toBeInTheDocument();
    });

    it("displays no recommendations message when no recommended products are available", async () => {
        vi.mocked(getRecommended).mockImplementation(async () => new Response(JSON.stringify([])));

        await act(async () => {
            render(<ProductHub user={mockUser} />);
        });

        expect(await screen.findByText("No recommendations available, make some purchases!")).toBeInTheDocument();
    });

    it("displays no results found message when search returns no products", async () => {
        vi.mocked(searchProducts).mockImplementation(async () => new Response(JSON.stringify([])));

        render(<ProductHub user={mockUser} />);

        const searchInput = screen.getByPlaceholderText("Search for products");
        const searchButton = screen.getByText("Search");

        fireEvent.change(searchInput, { target: { value: "Nonexistent" } });
        fireEvent.click(searchButton);

        expect(await screen.findByText("No results found")).toBeInTheDocument();
    });
});