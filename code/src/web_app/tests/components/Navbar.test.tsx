import {describe, it, expect, vi, beforeEach} from "vitest"
import {act, fireEvent, render, screen} from "@testing-library/react"
import Navbar from "../../src/components/Navbar";
import React from "react";
import { UserType } from "../../src/types/auth";
import { MemoryRouter, useNavigate } from "react-router-dom";

const mockCustomer = {
    username: "testuser",
    type: UserType.Customer,
    id: 1,
    name: "Test User",
}

const mockBusiness = {
    username: "testbusiness",
    type: UserType.Business,
    id: 2,
    business_name: "Test Business",
}

vi.mock("react-router-dom", async () => ({
    ...(await vi.importActual("react-router-dom")),
    useNavigate: vi.fn()
}));

describe("Tests for Navbar", () => {
    beforeEach(() => {
        sessionStorage.setItem('user', JSON.stringify(mockCustomer));
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
    })
    it("renders the logo", () => {
        render(
            <Navbar user={null} setUser={() => {}}/>
        );
        expect(screen.getByAltText("Wells Fargo Logo")).toBeInTheDocument();
    })
    it("renders the portal name for customer", () => {
        render(
            <Navbar user={mockCustomer} setUser={() => {}}/>
        );
        expect(screen.getByText("Prefinity")).toBeInTheDocument();
    })
    it("renders the portal name for business", () => {
        render(
            <Navbar user={mockBusiness} setUser={() => {}}/>
        );
        expect(screen.getByText("InsightGen")).toBeInTheDocument();
    })
    it("renders the user profile", () => {
        render(
            <Navbar user={mockCustomer} setUser={() => {}}/>
        );
        expect(screen.getByText("TESTUSER")).toBeInTheDocument();
    })
    it("renders the business name", () => {
        render(
            <Navbar user={mockBusiness} setUser={() => {}}/>
        );
        expect(screen.getByText("Test Business")).toBeInTheDocument();
    })
    it("navigates to /login when logout is clicked", async () => {
        const setUser = vi.fn();
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        render(
            <MemoryRouter>
            <Navbar user={mockCustomer} setUser={setUser}/>
            </MemoryRouter>
        )
        const userProfile = screen.getByText("TESTUSER");
        await act(async () => {
            fireEvent.click(userProfile);
        });

        screen.getByText("Logout").click();
        expect(setUser).toHaveBeenCalledWith(null);
        expect(mockNavigate).toHaveBeenCalledWith("/login");
    })
})