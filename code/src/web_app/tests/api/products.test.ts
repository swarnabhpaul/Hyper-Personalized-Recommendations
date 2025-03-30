import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getRecommended, searchProducts } from '../../src/api/products';
import { API_URL } from '../../src/api/config';

describe('API Products', () => {
    beforeEach(() => {
        global.fetch = vi.fn();
    });

    afterEach(() => {
        vi.resetAllMocks();
    });

    it('should fetch recommended products', async () => {
        const mockResponse = { data: 'recommended products' };
        vi.mocked(global.fetch).mockResolvedValue(new Response(JSON.stringify(mockResponse), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        }));

        const cid = 123;
        const response = await getRecommended(cid);
        const json = await response.json();

        expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/recommend?cid=${cid}`, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            },
        });
        expect(json).toEqual(mockResponse);
        });

        it('should fetch search products', async () => {
        const mockResponse = { data: 'search results' };
        vi.mocked(global.fetch).mockResolvedValue(new Response(JSON.stringify(mockResponse), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        }));

        const query = 'test';
        const response = await searchProducts(query);
        const json = await response.json();

        expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/search_products?query=${query}`, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            },
        });
        expect(json).toEqual(mockResponse);
        });

        it('should handle fetch errors for getRecommended', async () => {
        vi.mocked(global.fetch).mockResolvedValue(new Response(null, {
            status: 404,
            statusText: 'Not Found',
        }));

        const cid = 123;
        const response = await getRecommended(cid);

        expect(response.ok).toBe(false);
        expect(response.statusText).toBe('Not Found');
        });

        it('should handle fetch errors for searchProducts', async () => {
        vi.mocked(global.fetch).mockResolvedValue(new Response(null, {
            status: 404,
            statusText: 'Not Found',
        }));

        const query = 'test';
        const response = await searchProducts(query);

        expect(response.ok).toBe(false);
        expect(response.statusText).toBe('Not Found');
    });
});