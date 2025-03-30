import { useEffect, useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { User, UserType } from './types/auth.ts';
import Navbar from './components/Navbar';
import CustomerPortal from './components/CustomerPortal.tsx';
import BusinessPortal from './components/BusinessPortal.tsx';
import Login from './components/Login.tsx';
import { getUser, setUser as setUserInStorage } from './utils/auth.ts';
import ProductHub from './components/ProductHub.tsx';
import MyFin from './components/MyFin.tsx';

const excludedPaths = ['/login']

function App() {
  const [user, setUser] = useState<User|null>(getUser());

  useEffect(() => {
    setUserInStorage(user);
  }, [user])

  if(!user && !excludedPaths.includes(location.pathname)) {
    location.pathname = '/login'
  }

  return (
    <div className = "app-container">
      <Router>
        <Navbar user={user} setUser={setUser}/>
        <Routes>
          <Route path="/" element={
            user && (user.type == UserType.Customer ?
              <CustomerPortal />
            : <BusinessPortal user={user}/>)
          }>
            <Route path="/products" element={<ProductHub user={user}/>} />
            <Route path="/myfin" element={<MyFin user={user}/>} />
          </Route>
          <Route path="/login" element={<Login user={user} setUser={setUser} />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App