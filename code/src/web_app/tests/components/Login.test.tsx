import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MemoryRouter, Route, Routes, useNavigate } from 'react-router-dom';
import Login from '../../src/components/Login';
import { User, UserType } from '../../src/types/auth';
import React from "react";
import { loginRequest } from '../../src/api/auth';

vi.mock('react-router-dom', async () => ({
    ...(await vi.importActual('react-router-dom')),
    useNavigate: vi.fn(),
}));

vi.mock('../../src/api/auth', () => ({
    loginRequest: vi.fn(),
}));

const mockCustomer = {
    username: "c123",
    name: "Test User",
}

const mockBusiness = {
    username: "c123",
    business_name: "Test User",
}

describe('Login Component', () => {
    const mockSetUser = vi.fn();

    const renderComponent = (user: User | null) => {
        render(
            <MemoryRouter initialEntries={['/login']}>
                <Routes>
                    <Route path="/login" element={<Login user={user} setUser={mockSetUser} />} />
                </Routes>
            </MemoryRouter>
        );
    };

    it('renders the login form', () => {
        renderComponent(null);
        expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
        expect(screen.getByText(/submit/i)).toBeInTheDocument();
        expect(screen.getByText(/reset/i)).toBeInTheDocument();
    });

    it('calls setUser with null if user is provided', () => {
        const globalRef = global;
        globalRef.location = {...global.location, pathname: '/login'}
        const user: User = { username: 'testuser', id: 1, type: UserType.Customer };
        renderComponent(user);
        expect(mockSetUser).toHaveBeenCalledWith(null);
    });

    it('calls loginRequest with username and password and navigates to root route', async () => {
        const username = 'c123';
        const password = 'testpassword';
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        vi.mocked(loginRequest).mockResolvedValue(new Response(JSON.stringify(mockCustomer), { status: 200 }));
        renderComponent(null);
        
        fireEvent.change(screen.getByLabelText(/username/i), { target: { value: username } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: password } });
        await act(async () => {
            fireEvent.click(screen.getByRole('button', { name: /submit/i }));
        });
        expect(vi.mocked(loginRequest)).toHaveBeenCalledWith(username, password);
        expect(mockNavigate).toBeCalledWith('/');
    });

    it('successfully logs in as business user', async () => {
        const username = 'b123';
        const password = 'testpassword';
        const mockNavigate = vi.fn();
        vi.mocked(useNavigate).mockReturnValue(mockNavigate);
        vi.mocked(loginRequest).mockResolvedValue(new Response(JSON.stringify(mockBusiness), { status: 200 }));
        renderComponent(null);
        
        fireEvent.change(screen.getByLabelText(/username/i), { target: { value: username } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: password } });
        await act(async () => {
            fireEvent.click(screen.getByRole('button', { name: /submit/i }));
        });
        expect(vi.mocked(loginRequest)).toHaveBeenCalledWith(username, password);
        expect(mockNavigate).toBeCalledWith('/');
    });

    it('displays error on wrong credentials', async () => {
        const username = 'testuser';
        const password = 'wrongpassword';
        vi.mocked(loginRequest).mockResolvedValue(new Response(JSON.stringify({detail: "error message"}), { status: 401 }));
        vi.mocked(useNavigate).mockReturnValue(vi.fn());
        renderComponent(null);

        fireEvent.change(screen.getByLabelText(/username/i), { target: { value: username } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: password } });
        await act(async () => {
            fireEvent.click(screen.getByRole('button', { name: /submit/i }));
        });

        expect(vi.mocked(loginRequest)).toHaveBeenCalledWith(username, password);
        expect(screen.getByText(/error message/i)).toBeInTheDocument();
    });

});