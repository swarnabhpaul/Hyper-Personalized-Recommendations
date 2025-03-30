import { useEffect, useState } from "react";
import { User } from "../types/auth";
import { getRecommended, searchProducts } from "../api/products";
import { Product } from "../types/product";

interface ProductHubProps {
    user: User|null;
}

function ProductHub({user}: ProductHubProps) {

    const [recommendedProducts, setRecommendedProducts] = useState<Product[]|null>(null);
    const [searchResults, setSearchResults] = useState<Product[]|null>(null);
    const [searchQuery, setSearchQuery] = useState<string>("");

    useEffect(() => {
        const getRecommendations = async () => {
            const res = await getRecommended(user?.id as number)
            const jsonRes = await res.json();
            if(Array.isArray(jsonRes) && jsonRes.length > 0) {
                setRecommendedProducts(jsonRes)
            }
        }

        if(user) {
            getRecommendations()
        }
    }, [user]);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault()
        const formData = new FormData(e.target as HTMLFormElement);
        const query = formData.get("query") as string;
        setSearchQuery(query);
        const res = await searchProducts(query);
        const jsonRes = await res.json();
        setSearchResults(jsonRes);
    }

    return (
        <>
            <h1 className="customer-portal-heading">Products Hub</h1>
            <form className="product-search" onSubmit={handleSearch}>
                <input required name="query" type="text" placeholder="Search for products"/>
                <button type="submit">Search</button>
                <button onClick={() => setSearchResults(null)} type="reset">Reset</button>
            </form>
            <div className="product-display">
                {searchResults === null && (
                <div className="recommended-products">
                    <h2>Recommended Products</h2>
                    <p>Based on your previous purchases and purchases made by similar customers</p>
                    <p>Search something to see other products.</p>
                    <div className="product-carousel">
                        {recommendedProducts?.map((product) => {
                            return (
                                <div className="product-card">
                                    <h3>{product.product_name}</h3>
                                    <p>{product.business_name}</p>
                                </div>
                            )
                        })}
                        {recommendedProducts === null && <p>No recommendations available, make some purchases!</p>}
                    </div>
                </div>)}
                {searchResults && (
                <div className="search-results">
                    <h2>Search Results for "{searchQuery}"</h2>
                    <div className="product-carousel">
                        {searchResults.map((product) => {
                            return (
                                <div className="product-card">
                                    <h3>{product.product_name}</h3>
                                    <p>{product.business_name}</p>
                                </div>
                            )
                        })}
                        {searchResults.length === 0 && <p>No results found</p>}
                    </div>
                </div>
                )}
            </div>
        </>
    )
}

export default ProductHub