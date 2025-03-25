import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Container,
  Card,
  CardBody,
  CardTitle,
  CardText,
  Button,
  Spinner,
  Row,
  Col,
} from "reactstrap";
import AuthContext from "../context/AuthContext";

const Profile = () => {
  const { user, logout, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !user) {
      navigate("/login");
    }
  }, [loading, user, navigate]);

  if (loading) {
    return (
      <Container className="mt-5 text-center">
        <Spinner color="primary" />
      </Container>
    );
  }

  if (!user) return null;

  return (
    <Container className="mt-5 d-flex justify-content-center">
      <Card className="shadow-lg p-4" style={{ maxWidth: "500px", width: "100%" }}>
        <CardBody className="text-center">
          <CardTitle tag="h2">{user.name || "Unknown"}</CardTitle>
          <CardText className="text-muted">{user.email || "Unknown"}</CardText>
          <CardText>
            <strong>Role:</strong> {user.role}
          </CardText>
        </CardBody>
      </Card>
    </Container>
  );
};

export default Profile;
