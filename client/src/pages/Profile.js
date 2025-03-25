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
  Badge,
} from "reactstrap";
import { FaUserCircle, FaEnvelope, FaSignOutAlt, FaUserShield } from "react-icons/fa";
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
        <Spinner color="primary" size="lg" />
      </Container>
    );
  }

  if (!user) return null;

  return (
    <Container className="mt-5 d-flex justify-content-center">
      <Card className="shadow-lg p-4 text-center border-0" style={{ maxWidth: "500px", width: "100%" }}>
        <CardBody>
          {/* Profile Picture */}
          <FaUserCircle size={90} className="text-secondary mb-3" />

          {/* Name */}
          <CardTitle tag="h2" className="text-dark">
            {user.name || "Unknown"}
          </CardTitle>

          {/* Email */}
          <CardText className="text-muted">
            <FaEnvelope className="me-2" />
            {user.email || "Unknown"}
          </CardText>

          {/* Role Badge */}
          <CardText>
            <Badge color={user.role === "admin" ? "danger" : "primary"} className="p-2">
              <FaUserShield className="me-1" /> {user.role.toUpperCase()}
            </Badge>
          </CardText>

          {/* Additional Info */}
          <CardText className="mt-3 text-muted">
            Welcome to your profile! You can manage your account and explore your dashboard.
          </CardText>

          {/* Logout Button */}
          <Button
            color="danger"
            className="mt-3"
            onClick={() => {
              if (window.confirm("Are you sure you want to logout?")) {
                logout();
              }
            }}
          >
            <FaSignOutAlt className="me-2" /> Logout
          </Button>
        </CardBody>
      </Card>
    </Container>
  );
};

export default Profile;
