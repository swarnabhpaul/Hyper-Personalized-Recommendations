import { describe, it, expect, vi, beforeEach } from 'vitest';
import { loginRequest } from '../../src/api/auth';
import { API_URL } from '../../src/api/config';

describe('loginRequest', () => {
    const username = 'testuser';
    const password = 'testpassword';

    beforeEach(() => {
        global.fetch = vi.fn();
    });

    it('should call fetch with the correct URL and options', async () => {
        const mockResponse = new Response(JSON.stringify({}), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
        vi.mocked(global.fetch).mockResolvedValue(mockResponse);

        await loginRequest(username, password);

        expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/login`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        });

        it('should return the response from fetch', async () => {
            const mockResponse = new Response(JSON.stringify({}), {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            });
            vi.mocked(global.fetch).mockResolvedValue(mockResponse);

            const response = await loginRequest(username, password);

            expect(response).toEqual(mockResponse);
        });

        it('should handle fetch errors', async () => {
            const mockError = new Error('Fetch failed');
            vi.mocked(global.fetch).mockRejectedValue(mockError);

            await expect(loginRequest(username, password)).rejects.toThrow('Fetch failed');
    });
});