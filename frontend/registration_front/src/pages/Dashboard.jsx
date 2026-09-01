import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";

function Dashboard() {

    const [student, setStudent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        const getDashboard = async () => {

            try {

                const response = await api.get(
                    "student/dashboard/"
                );

                setStudent(response.data.student);

            } catch (error) {

                console.error(error);

                setError(
                    "Could not load dashboard."
                );

            } finally {

                setLoading(false);

            }
        };

        getDashboard();

    }, []);

    if (loading) {
        return (
            <>
                <Navbar />
                <div className="container">
                    <h2>Loading...</h2>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Navbar />
                <div className="container">
                    <div className="error">
                        {error}
                    </div>
                </div>
            </>
        );
    }

    return (
        <>
            <Navbar />

            <main className="container">

                <h1>
                    Welcome, {student.first_name}
                </h1>

                <div className="student-card">

                    <h2>Student Information</h2>

                    <div className="info-grid">

                        <div>
                            <strong>
                                First Name
                            </strong>
                            <p>
                                {student.first_name}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Last Name
                            </strong>
                            <p>
                                {student.last_name}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Student Number
                            </strong>
                            <p>
                                {student.student_number}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Gender
                            </strong>
                            <p>
                                {student.gender}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Date of Birth
                            </strong>
                            <p>
                                {student.date_of_birth}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Entry Year
                            </strong>
                            <p>
                                {student.entry_year}
                            </p>
                        </div>

                        <div>
                            <strong>
                                National Code
                            </strong>
                            <p>
                                {student.national_code}
                            </p>
                        </div>

                        <div>
                            <strong>
                                Department
                            </strong>
                            <p>
                                {student.dep?.department_name}
                            </p>
                        </div>

                    </div>

                </div>

                <div className="dashboard-actions">

                    <Link
                        to="/registration"
                        className="dashboard-button"
                    >
                        Course Registration
                    </Link>

                    <Link
                        to="/history"
                        className="dashboard-button"
                    >
                        Course History
                    </Link>

                </div>

            </main>
        </>
    );
}

export default Dashboard;