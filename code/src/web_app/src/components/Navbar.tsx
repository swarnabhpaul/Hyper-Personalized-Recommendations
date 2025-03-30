import WellsFargoLogo from "../assets/Wells_Fargo_Bank.svg"
import { Outlet } from 'react-router-dom';
import { SetStateAction, useEffect, useState } from "react";
import ProfileMenu from "./ProfileMenu";
import { Business, Customer, User, UserType } from "../types/auth";

interface NavbarProps {
    user: User|null,
    setUser: React.Dispatch<SetStateAction<User|null>>
}

const Navbar = ({user, setUser}: NavbarProps) => {
    const [showProfileMenu, setShowProfileMenu] = useState(false);

    useEffect(() => {
        setShowProfileMenu(false);
    }, [user])

    return (
        <>
            <div className="navbar">
                <div className="navbar-banner">
                    <img alt="Wells Fargo Logo" className="nav-logo" src={WellsFargoLogo}/>
                    {user && <span className="portal-name">{user?.type === UserType.Customer? "Prefinity": "InsightGen"}</span>}
                </div>
                {user && (
                    <div>
                        <div className="profile-container">
                            <div onClick = {() => setShowProfileMenu(!showProfileMenu)} className="user-profile-photo">
                                {user.username.toUpperCase()}
                            </div>
                            <div className="user-name">
                                {user.type === UserType.Customer? (user as Customer).name: (user as Business).business_name}
                            </div>
                        </div>
                        {showProfileMenu && <ProfileMenu setUser={setUser}/>}
                    </div>
                )}
            </div>
            <Outlet />
        </>
    );
};

export default Navbar;