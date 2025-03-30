import { render } from "@testing-library/react"
import { MemoryRouter, Route, Routes, useNavigate } from "react-router-dom"
import { describe, it, expect, vi } from "vitest"
import CustomerPortal from "../../src/components/CustomerPortal"
import React from "react"

vi.mock("../../src/components/CustomerSideBar", () => ({
    default: () => <div>Mocked CustomerSideBar</div>,
}))

vi.mock('react-router-dom', async () => ({
    ...(await vi.importActual('react-router-dom')),
    useNavigate: vi.fn(),
}));

describe("CustomerPortal", () => {
    it("should redirect to /products if pathname is /", () => {
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate)
        const { container } = render(
            <MemoryRouter initialEntries={["/"]}>
                <Routes>
                    <Route path="*" element={<CustomerPortal />} />
                </Routes>
            </MemoryRouter>
        )
        expect(container.innerHTML).toContain("Mocked CustomerSideBar")
        expect(mockNavigate).toBeCalledWith("products")
    })

    it("should render CustomerSideBar and Outlet", () => {
        const { container } = render(
            <MemoryRouter initialEntries={["/somepath"]}>
                <Routes>
                    <Route path="*" element={<CustomerPortal />} />
                </Routes>
            </MemoryRouter>
        )
        expect(container.innerHTML).toContain("Mocked CustomerSideBar")
    })
})