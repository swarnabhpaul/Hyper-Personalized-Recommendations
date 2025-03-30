import { API_URL } from "./config";

export async function getBusinessInsights(bid: number) {
    const response = await fetch(`${API_URL}/business_insight?bid=${bid}`);
    return response;
}