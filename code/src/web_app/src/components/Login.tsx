import { FormEvent, SetStateAction, useEffect, useState } from "react"
import { User, UserType } from "../types/auth"
import { loginRequest } from "../api/auth";
import { useLocation, useNavigate } from "react-router-dom";

interface LoginProps {
    user: User|null
    setUser: React.Dispatch<SetStateAction<User|null>>
}

function Login({user, setUser}: LoginProps) {
    const [isError, setIsError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        if(location.pathname === "/login" && user) {
            setUser(null)
        }
    }, [user, setUser])

    const handleLogin = async (e: FormEvent) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form)
        const username = formData.get('username') as string;
        const password = formData.get('password') as string;

        form.reset();

        const res = await loginRequest(username, password)
        const jsonRes = await res.json()

        if(res.ok) {
            setUser({
                username,
                id: parseInt(username.slice(1)),
                type: username[0] == 'c'? UserType.Customer: UserType.Business,
                ...jsonRes
            })
            setIsError(false);
            setErrorMessage('');
            navigate('/')
        }
        else {
            setIsError(true);
            setErrorMessage(jsonRes.detail);
        }
    }

    return (
    <div className="login-container">
        <section className="login-hero">
            Prefinity & <br/>InsightGen
        </section>
        <div className="login-line" />
        <section className="login-form-container">
            <form onSubmit={handleLogin} className="login-form">
                <section className="form-section">
                    <label htmlFor="username">Username: </label>
                    <input required id="username" name="username" type="text"/>
                </section>
                <section className="form-section">
                    <label htmlFor="password">Password: </label>
                    <input required id="password" name="password" type="password"/>
                </section>
                <section className="submit-section">
                    <button type="submit">Submit</button>
                    <button type="reset">Reset</button>
                </section> 
            </form>
            {isError && <p title={`Error: ${errorMessage}, click to dismiss`} onClick={() => {setIsError(false)}} className="form-error">{errorMessage}</p>}
        </section>
    </div>
    )
}

export default Login