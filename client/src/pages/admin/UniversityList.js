import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, Button, Container, Spinner, Row, Col, Card, CardBody, Alert } from "reactstrap";
import { FaArrowLeft, FaTrash } from "react-icons/fa";

const UniversityList = () => {
  const [universities, setUniversities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const res = await axios.get("http://localhost:6969/api/universities");
        setUniversities(res.data.universities || []);
      } catch (error) {
        setError("Failed to fetch universities. Please try again.");
        console.error("Error fetching universities:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUniversities();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this university?")) return;

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No token found");
      return;
    }

    try {
      await axios.delete(`http://localhost:6969/api/universities/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUniversities((prev) => prev.filter((uni) => uni._id !== id));
    } catch (error) {
      setError("Failed to delete university.");
      console.error("Error deleting university:", error);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="mb-3">
        <Col>
          <Button color="secondary" onClick={() => navigate(-1)}>
            <FaArrowLeft /> Go Back
          </Button>
        </Col>
      </Row>

      <Card className="shadow">
        <CardBody>
          <h2 className="text-center text-primary">Manage Universities</h2>

          {loading ? (
            <div className="text-center my-4">
              <Spinner color="primary" />
            </div>
          ) : error ? (
            <Alert color="danger">{error}</Alert>
          ) : universities.length === 0 ? (
            <Alert color="info" className="text-center">No universities found.</Alert>
          ) : (
            <Table bordered hover responsive className="mt-3">
              <thead className="table-dark text-center">
                <tr>
                  <th>Name</th>
                  <th>Location</th>
                  <th>Ranking</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {universities.map((uni) => (
                  <tr key={uni._id}>
                    <td>{uni.name}</td>
                    <td>{uni.location}</td>
                    <td>{uni.ranking}</td>
                    <td className="text-center">
                      <Button color="danger" size="sm" onClick={() => handleDelete(uni._id)}>
                        <FaTrash /> Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </CardBody>
      </Card>
    </Container>
  );
};

export default UniversityList;
