import React from 'react'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter as Router } from 'react-router-dom'
import { describe, it, vi, expect, beforeEach } from 'vitest'
import App from '../src/App'
import { getUser } from '../src/utils/auth'
import { UserType } from '../src/types/auth'

vi.mock('../src/utils/auth', () => ({
    getUser: vi.fn(),
    setUser: vi.fn()
}))

vi.mock('../src/components/Navbar', () => ({
    __esModule: true,
    default: () => <div>Mocked Navbar</div>
}))

vi.mock('../src/components/CustomerPortal', () => ({
    __esModule: true,
    default: () => <div>Mocked CustomerPortal</div>
}))

vi.mock('../src/components/BusinessPortal', () => ({
    __esModule: true,
    default: () => <div>Mocked BusinessPortal</div>
}))

vi.mock('../src/components/Login', () => ({
    __esModule: true,
    default: () => <div>Mocked Login</div>
}))

vi.mock('../src/components/ProductHub', () => ({
    __esModule: true,
    default: () => <div>Mocked ProductHub</div>
}))

vi.mock('../src/components/MyFin', () => ({
    __esModule: true,
    default: () => <div>Mocked MyFin</div>
}))

describe('App component', () => {

    beforeEach(() => {
        const globalRef = global;
        globalRef.location = {...location, pathname: '/'}
    })

    it('renders login page if no user is found', async () => {
        vi.mocked(getUser).mockReturnValue(null);
        await act(async () => {
            render(
            <App />
            )
        })
        expect(location.pathname).toEqual('/login')
    })

    it('renders CustomerPortal if user is a customer', () => {
        vi.mocked(getUser).mockReturnValue({ type: UserType.Customer })
        render(
            <App />
        )
        expect(screen.getByText('Mocked CustomerPortal')).toBeInTheDocument()
    })

    it('renders BusinessPortal if user is a business', () => {
        vi.mocked(getUser).mockReturnValue({ type: UserType.Business })
        render(
            <App />
        )
        expect(screen.getByText('Mocked BusinessPortal')).toBeInTheDocument()
    })
})