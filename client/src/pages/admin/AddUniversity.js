import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { 
  Container, Form, FormGroup, Label, Input, Button, 
  Alert, Row, Col, Card, CardBody 
} from "reactstrap";
import { FaArrowLeft } from "react-icons/fa";

const AddUniversity = () => {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [ranking, setRanking] = useState("");
  const [description, setDescription] = useState("");
  const [website, setWebsite] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleAddUniversity = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("You must be logged in to add a university.");
      setLoading(false);
      return;
    }

    try {
      await axios.post(
        "http://localhost:6969/api/universities",
        { name, location, ranking, description, website },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setSuccess(true);
      setName("");
      setLocation("");
      setRanking("");
      setDescription("");
      setWebsite("");

      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add university. Please try again.");
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

              <h2 className="text-center text-primary">Add a University</h2>
              
              {error && <Alert color="danger">{error}</Alert>}
              {success && <Alert color="success">University added successfully!</Alert>}
              
              <Form onSubmit={handleAddUniversity}>
                <FormGroup>
                  <Label for="name">University Name</Label>
                  <Input 
                    type="text" id="name" placeholder="Enter university name" 
                    value={name} onChange={(e) => setName(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="location">Location</Label>
                  <Input 
                    type="text" id="location" placeholder="Enter location" 
                    value={location} onChange={(e) => setLocation(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="ranking">Ranking</Label>
                  <Input 
                    type="number" id="ranking" placeholder="Enter ranking (e.g., 1, 50, 100)" 
                    value={ranking} onChange={(e) => setRanking(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="description">Description</Label>
                  <Input 
                    type="textarea" id="description" placeholder="Short description about the university" 
                    value={description} onChange={(e) => setDescription(e.target.value)} 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="website">Website</Label>
                  <Input 
                    type="url" id="website" placeholder="https://example.com" 
                    value={website} onChange={(e) => setWebsite(e.target.value)} 
                  />
                </FormGroup>

                <Button color="primary" type="submit" disabled={loading} block>
                  {loading ? "Adding..." : "Add University"}
                </Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AddUniversity;
