import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Form, FormGroup, Label, Input, Button, Alert } from "reactstrap";

const AddProgram = () => {
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");
  const [degreeType, setDegreeType] = useState("");
  const [university, setUniversity] = useState("");
  const [universities, setUniversities] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const response = await axios.get("http://localhost:6969/api/universities");
        setUniversities(response.data.universities);
      } catch (error) {
        console.error("Error fetching universities:", error);
      }
    };

    fetchUniversities();
  }, []);

  const handleAddProgram = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No token found");
      return;
    }

    try {
      await axios.post("http://localhost:6969/api/programs", { name, duration, degreeType, university }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSuccess(true);
      setName("");
      setDuration("");
      setDegreeType("");
      setUniversity("");
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add program. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <h2>Add Program</h2>
      {error && <Alert color="danger">{error}</Alert>}
      {success && <Alert color="success">Program added successfully!</Alert>}
      <Form onSubmit={handleAddProgram}>
        <FormGroup>
          <Label for="name">Name</Label>
          <Input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="duration">Duration</Label>
          <Input type="text" id="duration" value={duration} onChange={(e) => setDuration(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="degreeType">Degree Type</Label>
          <Input type="text" id="degreeType" value={degreeType} onChange={(e) => setDegreeType(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="university">University</Label>
          <Input type="select" id="university" value={university} onChange={(e) => setUniversity(e.target.value)} required>
            <option value="">Select University</option>
            {universities.map((uni) => (
              <option key={uni._id} value={uni._id}>{uni.name}</option>
            ))}
          </Input>
        </FormGroup>
        <Button color="primary" type="submit">Add Program</Button>
      </Form>
    </Container>
  );
};

export default AddProgram;