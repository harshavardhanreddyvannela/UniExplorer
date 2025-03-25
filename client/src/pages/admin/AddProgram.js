import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { 
  Container, Form, FormGroup, Label, Input, Button, 
  Alert, Row, Col, Card, CardBody 
} from "reactstrap";
import { FaArrowLeft } from "react-icons/fa";

const AddProgram = () => {
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");
  const [degreeType, setDegreeType] = useState("");
  const [university, setUniversity] = useState("");
  const [universities, setUniversities] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const response = await axios.get("http://localhost:6969/api/universities");
        setUniversities(response.data.universities);
      } catch (error) {
        console.error("Error fetching universities:", error);
        setError("Failed to load universities. Try refreshing.");
      }
    };

    fetchUniversities();
  }, []);

  const handleAddProgram = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("You must be logged in to add a program.");
      setLoading(false);
      return;
    }

    try {
      await axios.post(
        "http://localhost:6969/api/programs",
        { name, duration, degreeType, university },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setSuccess(true);
      setName("");
      setDuration("");
      setDegreeType("");
      setUniversity("");

      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add program. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="shadow-sm">
            <CardBody>
              <Button color="secondary" className="mb-3" onClick={() => navigate(-1)}>
                <FaArrowLeft /> Go Back
              </Button>

              <h2 className="text-center text-primary">Add a New Program</h2>
              
              {error && <Alert color="danger">{error}</Alert>}
              {success && <Alert color="success">Program added successfully!</Alert>}
              
              <Form onSubmit={handleAddProgram}>
                <FormGroup>
                  <Label for="name">Program Name</Label>
                  <Input 
                    type="text" id="name" placeholder="Enter program name" 
                    value={name} onChange={(e) => setName(e.target.value)} required 
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label for="duration">Duration</Label>
                  <Input 
                    type="text" id="duration" placeholder="e.g., 4 years" 
                    value={duration} onChange={(e) => setDuration(e.target.value)} required 
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label for="degreeType">Degree Type</Label>
                  <Input 
                    type="text" id="degreeType" placeholder="e.g., BSc, MSc" 
                    value={degreeType} onChange={(e) => setDegreeType(e.target.value)} required 
                  />
                </FormGroup>
                
                <FormGroup>
                  <Label for="university">University</Label>
                  <Input 
                    type="select" id="university" value={university} 
                    onChange={(e) => setUniversity(e.target.value)} required
                  >
                    <option value="">Select University</option>
                    {universities.map((uni) => (
                      <option key={uni._id} value={uni._id}>{uni.name}</option>
                    ))}
                  </Input>
                </FormGroup>

                <Button color="primary" type="submit" disabled={loading}>
                  {loading ? "Adding..." : "Add Program"}
                </Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AddProgram;
