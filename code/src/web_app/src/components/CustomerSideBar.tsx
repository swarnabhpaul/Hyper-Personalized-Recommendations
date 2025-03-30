import { useNavigate } from "react-router-dom"

function CustomerSideBar() {
    const navigate = useNavigate();

    return (
        <div className="customer-sidebar">
            <div className="customer-sidebar-handle">=</div>
            <button onClick={() => navigate('products')}>Products Hub</button>
            <button onClick={() => navigate('myfin')}>MyFin</button>
        </div>
    )
}

export default CustomerSideBar