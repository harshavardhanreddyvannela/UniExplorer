import React, { useState } from "react";
import axios from "axios";
import { Container, Form, FormGroup, Label, Input, Button, Alert } from "reactstrap";

const AddUniversity = () => {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [ranking, setRanking] = useState("");
  const [description, setDescription] = useState("");
  const [website, setWebsite] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleAddUniversity = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No token found");
      return;
    }

    try {
      await axios.post("http://localhost:6969/api/universities", { name, location, ranking, description, website }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSuccess(true);
      setName("");
      setLocation("");
      setRanking("");
      setDescription("");
      setWebsite("");
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add university. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <h2>Add University</h2>
      {error && <Alert color="danger">{error}</Alert>}
      {success && <Alert color="success">University added successfully!</Alert>}
      <Form onSubmit={handleAddUniversity}>
        <FormGroup>
          <Label for="name">Name</Label>
          <Input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="location">Location</Label>
          <Input type="text" id="location" value={location} onChange={(e) => setLocation(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="ranking">Ranking</Label>
          <Input type="number" id="ranking" value={ranking} onChange={(e) => setRanking(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="description">Description</Label>
          <Input type="textarea" id="description" value={description} onChange={(e) => setDescription(e.target.value)} />
        </FormGroup>
        <FormGroup>
          <Label for="website">Website</Label>
          <Input type="url" id="website" value={website} onChange={(e) => setWebsite(e.target.value)} />
        </FormGroup>
        <Button color="primary" type="submit">Add University</Button>
      </Form>
    </Container>
  );
};

export default AddUniversity;