import { API_URL } from "./config";

export async function getBusinessKPI(bid: number) {
    const response = await fetch(`${API_URL}/business_chart?bid=${bid}`);
    return response;
}