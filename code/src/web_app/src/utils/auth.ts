import { User } from "../types/auth"

export const getUser = (): User|null => {
    const userString = sessionStorage.getItem("user")
    return userString? JSON.parse(userString): null;
}

export const setUser = (user: User|null) => {
    if(!user) {
        sessionStorage.removeItem('user');
    }
    else {
        sessionStorage.setItem("user", JSON.stringify(user));
    }
}