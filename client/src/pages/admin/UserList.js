import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, Button, Container, Spinner, Row, Col, Card, CardBody, Alert } from "reactstrap";
import { FaArrowLeft, FaTrash } from "react-icons/fa";

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("No token found");
        return;
      }

      try {
        const response = await axios.get("http://localhost:6969/api/admin/users", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(response.data);
      } catch (error) {
        setError("Failed to fetch users. Please try again.");
        console.error("Error fetching users:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;

    const token = localStorage.getItem("token");
    if (!token) {
      setError("No token found");
      return;
    }

    try {
      await axios.delete(`http://localhost:6969/api/admin/users/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers((prev) => prev.filter((user) => user._id !== id));
    } catch (error) {
      setError("Failed to delete user.");
      console.error("Error deleting user:", error);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="mb-3">
        <Col>
          <Button color="secondary" onClick={() => navigate(-1)}>
            <FaArrowLeft /> Go Back
          </Button>
        </Col>
      </Row>

      <Card className="shadow">
        <CardBody>
          <h2 className="text-center text-primary">User Management</h2>

          {loading ? (
            <div className="text-center my-4">
              <Spinner color="primary" />
            </div>
          ) : error ? (
            <Alert color="danger">{error}</Alert>
          ) : users.length === 0 ? (
            <Alert color="info" className="text-center">No users found.</Alert>
          ) : (
            <Table bordered hover responsive className="mt-3">
              <thead className="table-dark text-center">
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user, index) => (
                  <tr key={user._id}>
                    <td>{index + 1}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td className="text-center">
                      <Button color="danger" size="sm" onClick={() => handleDelete(user._id)}>
                        <FaTrash /> Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </CardBody>
      </Card>
    </Container>
  );
};

export default UserList;
