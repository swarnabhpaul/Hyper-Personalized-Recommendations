import { API_URL } from "./config";

export async function getRecommended(cid: number) {
    const res = await fetch(`${API_URL}/recommend?cid=${cid}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    return res;
}

export async function searchProducts(query: string) {
    const res = await fetch(`${API_URL}/search_products?query=${query}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    return res;
}