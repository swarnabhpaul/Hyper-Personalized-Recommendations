import {API_URL} from "./config"

export async function getLoanRecommendations(cid: number): 
Promise<Response> {
    const res = await fetch(`${API_URL}/loan_recommend?cid=${cid}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    return res;
}