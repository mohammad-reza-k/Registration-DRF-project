import { Link, useNavigate } from "react-router-dom";

function Navbar() {
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        navigate("/login");
    };

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <Link to="/dashboard">Student Portal</Link>
            </div>

            <div className="navbar-right">
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/registration">Registration</Link>
                <Link to="/history">History</Link>

                <button onClick={logout}>
                    Logout
                </button>
            </div>
        </nav>
    );
}

export default Navbar;