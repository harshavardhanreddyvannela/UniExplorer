import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { 
  Container, Form, FormGroup, Label, Input, Button, 
  Alert, Row, Col, Card, CardBody 
} from "reactstrap";
import { FaArrowLeft } from "react-icons/fa";

const AddUser = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleAddUser = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const token = localStorage.getItem("token");
    if (!token) {
      setError("You must be logged in to add a user.");
      setLoading(false);
      return;
    }

    try {
      await axios.post(
        "http://localhost:6969/api/auth/register",
        { name, email, password, role },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setSuccess(true);
      setName("");
      setEmail("");
      setPassword("");
      setRole("user");

      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      setError(error.response?.data?.message || "Failed to add user. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card className="shadow-sm">
            <CardBody>
              <Button color="secondary" className="mb-3" onClick={() => navigate(-1)}>
                <FaArrowLeft /> Go Back
              </Button>

              <h2 className="text-center text-primary">Add User</h2>
              
              {error && <Alert color="danger">{error}</Alert>}
              {success && <Alert color="success">User added successfully!</Alert>}
              
              <Form onSubmit={handleAddUser}>
                <FormGroup>
                  <Label for="name">Full Name</Label>
                  <Input 
                    type="text" id="name" placeholder="Enter full name" 
                    value={name} onChange={(e) => setName(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="email">Email Address</Label>
                  <Input 
                    type="email" id="email" placeholder="Enter email" 
                    value={email} onChange={(e) => setEmail(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="password">Password</Label>
                  <Input 
                    type="password" id="password" placeholder="Enter password" 
                    value={password} onChange={(e) => setPassword(e.target.value)} required 
                  />
                </FormGroup>

                <FormGroup>
                  <Label for="role">Role</Label>
                  <Input 
                    type="select" id="role" value={role} 
                    onChange={(e) => setRole(e.target.value)} required
                  >
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                  </Input>
                </FormGroup>

                <Button color="primary" type="submit" disabled={loading} block>
                  {loading ? "Adding..." : "Add User"}
                </Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AddUser;
