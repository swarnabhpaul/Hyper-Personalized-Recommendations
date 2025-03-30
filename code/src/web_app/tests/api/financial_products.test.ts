import { describe, it, expect, vi } from 'vitest';
import { getLoanRecommendations } from '../../src/api/financial_products';
import { API_URL } from '../../src/api/config';

describe('getLoanRecommendations', () => {
    it('should call fetch with the correct URL and headers', async () => {
        const cid = 123;
        const mockResponse = new Response(JSON.stringify({ data: 'test' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });

        global.fetch = vi.fn().mockResolvedValue(mockResponse);

        const response = await getLoanRecommendations(cid);

        expect(fetch).toHaveBeenCalledWith(`${API_URL}/loan_recommend?cid=${cid}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        expect(response).toBe(mockResponse);
    });

    it('should handle fetch errors', async () => {
        const cid = 123;
        const mockError = new Error('Fetch failed');

        global.fetch = vi.fn().mockRejectedValue(mockError);

        await expect(getLoanRecommendations(cid)).rejects.toThrow('Fetch failed');
    });
});