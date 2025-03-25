import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { Container, Card, CardBody, CardTitle, Form, FormGroup, Label, Input, Button, Alert } from "reactstrap";

const Login = () => {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors
    const success = await login(email, password);
    if (success) {
      setTimeout(()=>{navigate("/profile");},100);
    } else {
      setError("Invalid email or password. Please try again.");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
      <Card className="shadow p-4" style={{ maxWidth: "400px", width: "100%" }}>
        <CardBody>
          <CardTitle tag="h2" className="text-center mb-4">
            Login
          </CardTitle>

          {error && <Alert color="danger">{error}</Alert>}

          <Form onSubmit={handleLogin}>
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
              Login
            </Button>
          </Form>

          <p className="text-center mt-3">
            Don't have an account?{" "}
            <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => navigate("/register")}>
              Register here
            </span>
          </p>
        </CardBody>
      </Card>
    </Container>
  );
};

export default Login;
