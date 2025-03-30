import { useNavigate } from "react-router-dom"
import { User } from "../types/auth";
import { SetStateAction } from "react";

function ProfileMenu({setUser}: {setUser: React.Dispatch<SetStateAction<User|null>>}) {
    const navigate = useNavigate();

    const logout = () => {
        setUser(null);
        navigate('/login');
    }
    return (
        <div className="profile-menu">
            <button onClick = {logout}>Logout</button>
        </div>
    )
}

export default ProfileMenu