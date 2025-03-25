import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { 
  Container, Row, Col, Card, CardBody, CardTitle, Table, Spinner, Alert, Button 
} from "reactstrap";
import { FaArrowLeft } from "react-icons/fa";

const UniversityDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUniversityDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:6969/api/universities/${id}`);
        setUniversity(response.data);
      } catch (error) {
        console.error("Error fetching university details:", error);
        setError("Failed to load university details. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchUniversityDetails();
  }, [id]);

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner color="primary" />
        <p>Loading university details...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert color="danger">{error}</Alert>
      </Container>
    );
  }

  if (!university) {
    return (
      <Container className="mt-5 text-center">
        <h4>University not found</h4>
      </Container>
    );
  }

  return (
    <Container className="mt-4">
      {/* Go Back Button */}
      <Button color="secondary" className="mb-3" onClick={() => navigate("/universities")}>
        <FaArrowLeft className="me-2" /> Go Back to Universities
      </Button>

      <h2 className="mb-4 text-primary">{university.name}</h2>

      <Row>
        <Col md={8}>
          <Card className="mb-4 shadow">
            <CardBody>
              <CardTitle tag="h4" className="text-secondary">University Overview</CardTitle>
              <p><strong>Location:</strong> {university.location || "N/A"}</p>
              <p><strong>Ranking:</strong> #{university.ranking || "Not Ranked"}</p>
              <p><strong>Description:</strong> {university.description || "No description available."}</p>
            </CardBody>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="mb-4 text-center shadow">
            <CardBody>
              <CardTitle tag="h5" className="text-success">Total Programs</CardTitle>
              <h3>{university.programs.length}</h3>
            </CardBody>
          </Card>
        </Col>
      </Row>

      <Card className="mb-4 shadow">
        <CardBody>
          <CardTitle tag="h4" className="text-secondary">Available Programs</CardTitle>
          {university.programs.length > 0 ? (
            <Table striped bordered hover responsive>
              <thead className="table-dark">
                <tr>
                  <th>#</th>
                  <th>Program Name</th>
                  <th>Degree Level</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                {university.programs.map((program, index) => (
                  <tr key={program._id}>
                    <td>{index + 1}</td>
                    <td>{program.name}</td>
                    <td>{program.degree || "N/A"}</td>
                    <td>{program.duration || "N/A"}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          ) : (
            <p className="text-muted">No programs available.</p>
          )}
        </CardBody>
      </Card>
    </Container>
  );
};

export default UniversityDetails;
