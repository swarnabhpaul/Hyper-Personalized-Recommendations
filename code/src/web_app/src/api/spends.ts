import { API_URL } from "./config";

export async function getSpendsChartData(cid: number) {
    const res = await fetch(`${API_URL}/customer_chart?cid=${cid}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    return res;
}