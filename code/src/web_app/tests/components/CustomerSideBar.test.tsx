import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import CustomerSideBar from "../../src/components/CustomerSideBar";
import React from "react";
import { MemoryRouter, useNavigate } from "react-router-dom";

vi.mock('react-router-dom', async () => ({
    ...(await vi.importActual('react-router-dom')),
    useNavigate: vi.fn(),
}));

describe('Tests for CustomerSideBar', () => {
    it('should render correctly', () => {
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        render(
            <MemoryRouter>
                <CustomerSideBar />
            </MemoryRouter>
        );
        const productsHubButton = screen.getByText('Products Hub');
        expect(productsHubButton).toBeInTheDocument();
        const myFinButton = screen.getByText('MyFin');
        expect(myFinButton).toBeInTheDocument();
    });

    it('should navigate to products hub when products hub button is clicked', () => {
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        render(
            <MemoryRouter>
                <CustomerSideBar />
            </MemoryRouter>
        );
        const productsHubButton = screen.getByText('Products Hub');
        productsHubButton.click();
        expect(mockNavigate).toHaveBeenCalledWith('products');
    });

    it('should navigate to myfin when myfin button is clicked', () => {
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        render(
            <MemoryRouter>
                <CustomerSideBar />
            </MemoryRouter>
        );
        const myFinButton = screen.getByText('MyFin');
        myFinButton.click();
        expect(mockNavigate).toHaveBeenCalledWith('myfin');
    });

})