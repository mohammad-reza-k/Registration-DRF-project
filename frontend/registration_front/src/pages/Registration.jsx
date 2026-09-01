import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function Registration() {

    const [courses, setCourses] = useState([]);
    const [registrations, setRegistrations] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const [adding, setAdding] = useState(null);

    const getCourses = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await api.get(
                "registration/courses/"
            );

            setCourses(response.data);

        } catch (error) {

            console.error(error);

            setError(
                "Could not load course offerings."
            );

        } finally {

            setLoading(false);

        }
    };

    useEffect(() => {
        getCourses();
        getRegistrations();
    }, []);

    const addCourse = async (offeringId) => {

        try {

            setAdding(offeringId);
            setError("");
            setMessage("");

            const response = await api.post(
                `registration/add/${offeringId}/`
            );

            setMessage(
                response.data.message ||
                "Course added successfully."
            );

            await getCourses();
            await getRegistrations();

        } catch (error) {

            console.error("FULL ERROR:", error);

            const data = error.response?.data;

            let message = "Could not register for this course.";

            if (typeof data?.detail === "string") {
                message = data.detail;
            } 
            else if (Array.isArray(data?.detail)) {
                message = data.detail.join(" ");
            }
            else if (typeof data?.error === "string") {
                message = data.error;
            }

            setError(message);

        } finally {
            setAdding(null);
        }
    };

    const getRegistrations = async () => {
        try {
            const response = await api.get(
                "registration/list/"
            );

            setRegistrations(response.data);

        } catch (error) {
            console.error(error);

            const data = error.response?.data;

            setError(
                typeof data?.detail === "string"
                    ? data.detail
                    : "Could not load your registrations."
            );
        }
    };
    const finalizeCourse = async (enrollmentId) => {
        try {
            setError("");
            setMessage("");

            const response = await api.put(
                `registration/final/${enrollmentId}/`
            );

            setMessage(
                response.data.message ||
                "Course finalized successfully."
            );

            await getRegistrations();

        } catch (error) {
            console.error(error);

            const data = error.response?.data;

            let message = "Could not finalize course.";

            if (typeof data?.detail === "string") {
                message = data.detail;
            } else if (Array.isArray(data?.detail)) {
                message = data.detail.join(" ");
            }

            setError(message);
        }
    };

    const deleteCourse = async (enrollmentId) => {
        try {
            setError("");
            setMessage("");

            const response = await api.delete(
                `registration/delete/${enrollmentId}/`
            );

            setMessage(
                response.data.message ||
                "Course deleted successfully."
            );

            await getRegistrations();

        } catch (error) {
            console.error(error);

            const data = error.response?.data;

            let message = "Could not delete course.";

            if (typeof data?.detail === "string") {
                message = data.detail;
            } else if (Array.isArray(data?.detail)) {
                message = data.detail.join(" ");
            }

            setError(message);
        }
    };
    if (loading) {
        return (
            <>
                <Navbar />

                <main className="container">
                    <h2>Loading courses...</h2>
                </main>
            </>
        );
    }

    return (
        <>
            <Navbar />

            <main className="container">

                <h1>Course Registration</h1>

                {message && (
                    <div className="success">
                        {message}
                    </div>
                )}

                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}

                <div className="course-list">

                    {courses.length === 0 && (
                        <p>
                            No courses available.
                        </p>
                    )}

                    {courses.map((offering) => (

                        <div
                            className="course-card"
                            key={offering.id}
                        >

                            <div className="course-header">

                                <h2>
                                    {offering.course?.name}
                                </h2>

                                <span>
                                    {offering.course?.course_code}
                                </span>

                            </div>

                            <p>
                                {
                                    offering.course
                                        ?.description
                                }
                            </p>

                            <div className="course-details">

                                <div>
                                    <strong>
                                        Credits
                                    </strong>

                                    <span>
                                        {
                                            offering.course
                                                ?.credits
                                        }
                                    </span>
                                </div>

                                <div>
                                    <strong>
                                        Type
                                    </strong>

                                    <span>
                                        {
                                            offering.course
                                                ?.course_type
                                        }
                                    </span>
                                </div>

                                <div>
                                    <strong>
                                        Professor
                                    </strong>

                                    <span>
                                        {
                                            offering.prof
                                                ?.first_name
                                        }{" "}
                                        {
                                            offering.prof
                                                ?.last_name
                                        }
                                    </span>
                                </div>

                                <div>
                                    <strong>
                                        Semester
                                    </strong>

                                    <span>
                                        {
                                            offering.sem
                                                ?.term_name
                                        }
                                    </span>
                                </div>

                                <div>
                                    <strong>
                                        Capacity
                                    </strong>

                                    <span>
                                        {
                                            offering
                                                .registered_count
                                        }{" "}
                                        /{" "}
                                        {
                                            offering.capacity
                                        }
                                    </span>
                                </div>

                            </div>

                            <div className="course-actions">

                                <button
                                    onClick={() =>
                                        addCourse(
                                            offering.id
                                        )
                                    }
                                    disabled={
                                        adding ===
                                        offering.id
                                    }
                                >
                                    {adding ===
                                    offering.id
                                        ? "Adding..."
                                        : "Add Course"}
                                </button>

                            </div>

                        </div>

                    ))}

                </div>
                
                    <div className="registration-list">

                        <h2>My Registration</h2>

                        {loading && <p>Loading...</p>}

                        {error && (
                            <div className="error-message">
                                {error}
                            </div>
                        )}

                        {message && (
                            <div className="success-message">
                                {message}
                            </div>
                        )}

                        {!loading && registrations.length === 0 && (
                            <p>You have no registered courses.</p>
                        )}

                        {registrations.map((registration) => (

                            <div
                                key={registration.id}
                                className="registration-card"
                            >

                                <h3>{registration.course_name}</h3>

                                <p>
                                    Code: {registration.course_code}
                                </p>

                                <p>
                                    Credits: {registration.credits}
                                </p>

                                <p>
                                    Professor: {registration.professor}
                                </p>

                                <p>
                                    Status:{" "}
                                    <strong>
                                        {registration.status === "temp"
                                            ? "Temporary"
                                            : "Finalized"}
                                    </strong>
                                </p>

                                {registration.status === "temp" && (
                                    <div>

                                        <button
                                            onClick={() =>
                                                finalizeCourse(registration.id)
                                            }
                                        >
                                            Finalize
                                        </button>

                                        <button
                                            onClick={() =>
                                                deleteCourse(registration.id)
                                            }
                                        >
                                            Delete
                                        </button>

                                    </div>
                                )}

                            </div>

                        ))}

                </div>            

            </main>
        </>
    );
}

export default Registration;