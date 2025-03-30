import {describe, it, expect, vi} from "vitest"
import {render, screen} from "@testing-library/react"
import ProfileMenu from "../../src/components/ProfileMenu"
import React from "react";
import { MemoryRouter, useNavigate } from "react-router-dom";

vi.mock("react-router-dom", async () => ({
    ...(await vi.importActual("react-router-dom")),
    useNavigate: vi.fn(),
}));

describe("ProfileMenu", () => {
    it("renders a logout button", () => {
        render(
            <MemoryRouter>
                <ProfileMenu setUser={() => {}}/>
            </MemoryRouter>
        );
        expect(screen.getByText("Logout")).toBeInTheDocument();
    })
    it("navigates to /login when logout is clicked", () => {
        const setUser = vi.fn();
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        render(
            <MemoryRouter>
                <ProfileMenu setUser={setUser}/>
            </MemoryRouter>
        )
        screen.getByText("Logout").click();
        expect(setUser).toHaveBeenCalledWith(null);
        expect(mockNavigate).toHaveBeenCalledWith("/login");
    })
})