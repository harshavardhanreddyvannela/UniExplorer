import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, Button, Container, Spinner, Row, Col, Card, CardBody, Alert } from "reactstrap";
import { FaArrowLeft, FaTrash } from "react-icons/fa";

const ProgramList = () => {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        const res = await axios.get("http://localhost:6969/api/programs");
        setPrograms(res.data.programs);
      } catch (error) {
        setError("Failed to fetch programs. Please try again.");
        console.error("Error fetching programs:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPrograms();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this program?")) return;

    try {
      await axios.delete(`http://localhost:6969/api/programs/${id}`);
      setPrograms((prev) => prev.filter((prog) => prog._id !== id));
    } catch (error) {
      setError("Failed to delete program.");
      console.error("Error deleting program:", error);
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
          <h2 className="text-center text-primary">Manage Programs</h2>

          {loading ? (
            <div className="text-center my-4">
              <Spinner color="primary" />
            </div>
          ) : error ? (
            <Alert color="danger">{error}</Alert>
          ) : programs.length === 0 ? (
            <Alert color="info" className="text-center">No programs found.</Alert>
          ) : (
            <Table bordered hover responsive className="mt-3">
              <thead className="table-dark text-center">
                <tr>
                  <th>Name</th>
                  <th>Duration</th>
                  <th>Degree Type</th>
                  <th>University</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {programs.map((prog) => (
                  <tr key={prog._id}>
                    <td>{prog.name}</td>
                    <td>{prog.duration}</td>
                    <td>{prog.degreeType}</td>
                    <td>{prog.university?.name || "Unknown"}</td>
                    <td className="text-center">
                      <Button color="danger" size="sm" onClick={() => handleDelete(prog._id)}>
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

export default ProgramList;
