import { describe, it, expect, vi } from 'vitest';
import { getSpendsChartData } from '../../src/api/spends';
import { API_URL } from '../../src/api/config';

describe('getSpendsChartData', () => {
    it('should fetch spends chart data for a given customer id', async () => {
        const mockCid = 123;
        const mockResponse = new Response(JSON.stringify({ data: 'test data' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });

        global.fetch = vi.fn().mockResolvedValue(mockResponse);

        const res = await getSpendsChartData(mockCid);
        const data = await res.json();

        expect(fetch).toHaveBeenCalledWith(`${API_URL}/customer_chart?cid=${mockCid}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        expect(res.ok).toBe(true);
        expect(data).toEqual({ data: 'test data' });
    });

    it('should handle fetch errors', async () => {
        const mockCid = 123;
        global.fetch = vi.fn().mockRejectedValue(new Error('Fetch error'));

        await expect(getSpendsChartData(mockCid)).rejects.toThrow('Fetch error');
    });
});