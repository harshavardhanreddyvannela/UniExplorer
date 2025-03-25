import React, { useState } from "react";
import axios from "axios";
import { Container, Form, FormGroup, Label, Input, Button, Alert } from "reactstrap";

const AddUser = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleAddUser = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No token found");
      return;
    }

    try {
      await axios.post("http://localhost:6969/api/auth/register", { name, email, password, role }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSuccess(true);
      setName("");
      setEmail("");
      setPassword("");
      setRole("user");
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add user. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <h2>Add User</h2>
      {error && <Alert color="danger">{error}</Alert>}
      {success && <Alert color="success">User added successfully!</Alert>}
      <Form onSubmit={handleAddUser}>
        <FormGroup>
          <Label for="name">Name</Label>
          <Input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="email">Email</Label>
          <Input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="password">Password</Label>
          <Input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </FormGroup>
        <FormGroup>
          <Label for="role">Role</Label>
          <Input type="select" id="role" value={role} onChange={(e) => setRole(e.target.value)} required>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </Input>
        </FormGroup>
        <Button color="primary" type="submit">Add User</Button>
      </Form>
    </Container>
  );
};

export default AddUser;