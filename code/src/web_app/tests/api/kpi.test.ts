import { describe, it, expect, vi } from 'vitest';
import { getBusinessKPI } from '../../src/api/kpi';
import { API_URL } from '../../src/api/config';

describe('getBusinessKPI', () => {
    it('should fetch business KPI data for a given business ID', async () => {
        const mockResponse = { data: 'some data' };
        global.fetch = vi.fn(() =>
            Promise.resolve(new Response(JSON.stringify(mockResponse), {
                status: 200,
                headers: { 'Content-type': 'application/json' }
            }))
        );

        const bid = 123;
        const response = await getBusinessKPI(bid);
        const data = await response.json();

        expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/business_chart?bid=${bid}`);
        expect(data).toEqual(mockResponse);
    });

    it('should handle fetch errors', async () => {
        global.fetch = vi.fn(() => Promise.reject(new Error('Fetch error')));

        const bid = 123;
        await expect(getBusinessKPI(bid)).rejects.toThrow('Fetch error');
    });
});