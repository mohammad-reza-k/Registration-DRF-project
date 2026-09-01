import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function History() {

    const [history, setHistory] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        const getHistory = async () => {

            try {

                const response = await api.get(
                    "student/history/"
                );

                setHistory(
                    response.data.data || []
                );

            } catch (error) {

                console.error(error);

                setError(
                    "Could not load course history."
                );

            } finally {

                setLoading(false);

            }
        };

        getHistory();

    }, []);

    return (
        <>
            <Navbar />

            <main className="container">

                <h1>Course History</h1>

                {loading && (
                    <p>Loading...</p>
                )}

                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}

                {!loading &&
                    !error &&
                    history.length === 0 && (
                        <p>
                            No course history found.
                        </p>
                    )}

                {!loading &&
                    !error &&
                    history.length > 0 && (

                    <div className="table-container">

                        <table>

                            <thead>
                                <tr>
                                    <th>
                                        Course
                                    </th>

                                    <th>
                                        Credits
                                    </th>

                                    <th>
                                        Semester
                                    </th>

                                    <th>
                                        Professor
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                    <th>
                                        Enrollment Date
                                    </th>
                                </tr>
                            </thead>

                            <tbody>

                                {history.map(
                                    (course, index) => (

                                    <tr key={index}>

                                        <td>
                                            {
                                                course.course_name
                                            }
                                        </td>

                                        <td>
                                            {
                                                course.credits
                                            }
                                        </td>

                                        <td>
                                            {
                                                course.semester
                                            }
                                        </td>

                                        <td>
                                            {
                                                course
                                                    .professor_first_name
                                            }{" "}
                                            {
                                                course
                                                    .professor_last_name
                                            }
                                        </td>

                                        <td>
                                            {
                                                course.status
                                            }
                                        </td>

                                        <td>
                                            {
                                                new Date(
                                                    course
                                                        .enrollment_date
                                                ).toLocaleDateString()
                                            }
                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    </div>

                )}

            </main>
        </>
    );
}

export default History;