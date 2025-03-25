import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Container, Card, CardBody, CardTitle, Form, FormGroup, Label, Input, Button, Alert } from "reactstrap";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    try {
      await axios.post("http://localhost:6969/api/auth/register", { name, email, password });
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500);
    } catch (error) {
      setError(error.response?.data?.message || "Registration failed. Please try again.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
      <Card className="shadow p-4" style={{ maxWidth: "400px", width: "100%" }}>
        <CardBody>
          <CardTitle tag="h2" className="text-center mb-4">
            Register
          </CardTitle>

          {error && <Alert color="danger">{error}</Alert>}
          {success && <Alert color="success">Registration successful! Redirecting...</Alert>}

          <Form onSubmit={handleRegister}>
            <FormGroup>
              <Label for="name">Name</Label>
              <Input
                type="text"
                id="name"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </FormGroup>

            <FormGroup>
              <Label for="email">Email</Label>
              <Input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </FormGroup>

            <FormGroup>
              <Label for="password">Password</Label>
              <Input
                type="password"
                id="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </FormGroup>

            <Button color="primary" block className="mt-3">
              Register
            </Button>
          </Form>

          <p className="text-center mt-3">
            Already have an account?{" "}
            <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => navigate("/login")}>
              Login here
            </span>
          </p>
        </CardBody>
      </Card>
    </Container>
  );
};

export default Register;
