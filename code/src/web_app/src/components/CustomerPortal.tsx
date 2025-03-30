import { Outlet, useLocation, useNavigate } from "react-router-dom"
import CustomerSideBar from "./CustomerSideBar"
import { useEffect } from "react"

function CustomerPortal() {
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    if (location.pathname === "/") {
      navigate("products")
    }
  }, [location.pathname, navigate])

  return (
    <div className="customer-portal-container">
      <CustomerSideBar />
      <Outlet />
    </div>
  )
}

export default CustomerPortal