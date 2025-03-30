import { describe, it, expect, vi } from 'vitest';
import { getBusinessInsights } from '../../src/api/business_insights';
import { API_URL } from '../../src/api/config';

describe('getBusinessInsights', () => {
    it('should fetch business insights with the correct URL', async () => {
        const bid = 123;
        const mockResponse = { data: 'test data' };
        global.fetch = vi.fn().mockResolvedValue({
            json: vi.fn().mockResolvedValue(mockResponse),
        });

        const response = await getBusinessInsights(bid);
        const jsonResponse = await response.json();

        expect(fetch).toHaveBeenCalledWith(`${API_URL}/business_insight?bid=${bid}`);
        expect(jsonResponse).toEqual(mockResponse);
    });

    it('should handle fetch errors', async () => {
        const bid = 123;
        global.fetch = vi.fn().mockRejectedValue(new Error('Fetch error'));

        await expect(getBusinessInsights(bid)).rejects.toThrow('Fetch error');
    });
});