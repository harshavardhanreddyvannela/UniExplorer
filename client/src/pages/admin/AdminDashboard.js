import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Container, Row, Col, Card, CardBody, CardTitle, Button, Spinner, Alert } from "reactstrap";
import { FaUniversity, FaBook, FaUsers, FaPlus, FaTools, FaExclamationCircle, FaCheckCircle } from "react-icons/fa";

const AdminDashboard = () => {
  const [stats, setStats] = useState({ universities: 0, programs: 0, users: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("No token found");
        return;
      }

      try {
        const uniRes = await axios.get("http://localhost:6969/api/universities", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const progRes = await axios.get("http://localhost:6969/api/programs", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const userRes = await axios.get("http://localhost:6969/api/admin/users", {
          headers: { Authorization: `Bearer ${token}` },
        });

        setStats({
          universities: uniRes.data.universities.length,
          programs: progRes.data.programs.length,
          users: userRes.data.length,
        });
      } catch (error) {
        setError("Error fetching dashboard data. Please try again.");
        console.error("Error fetching stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <Container className="mt-5">
      <h2 className="text-center text-primary mb-4">
        <FaTools /> Admin Dashboard
      </h2>

      {loading ? (
        <div className="text-center my-5">
          <Spinner color="primary" size="lg" />
        </div>
      ) : error ? (
        <Alert color="danger" className="text-center">{error}</Alert>
      ) : (
        <>
          <Row className="justify-content-center mb-4">
            {/* Universities Card */}
            <Col md={4} className="mb-4">
              <Card className="text-center shadow border-0 bg-light">
                <CardBody>
                  <FaUniversity size={50} className="text-primary mb-2" />
                  <CardTitle tag="h5" className="text-dark">Total Universities</CardTitle>
                  <h3 className="text-primary font-weight-bold">{stats.universities}</h3>
                  <div className="d-grid gap-2 mt-3">
                    <Link to="/admin/universities" className="btn btn-outline-primary">Manage</Link>
                    <Button color="primary" tag={Link} to="/admin/universities/add">
                      <FaPlus /> Add University
                    </Button>
                  </div>
                </CardBody>
              </Card>
            </Col>

            {/* Programs Card */}
            <Col md={4} className="mb-4">
              <Card className="text-center shadow border-0 bg-light">
                <CardBody>
                  <FaBook size={50} className="text-success mb-2" />
                  <CardTitle tag="h5" className="text-dark">Total Programs</CardTitle>
                  <h3 className="text-success font-weight-bold">{stats.programs}</h3>
                  <div className="d-grid gap-2 mt-3">
                    <Link to="/admin/programs" className="btn btn-outline-success">Manage</Link>
                    <Button color="success" tag={Link} to="/admin/programs/add">
                      <FaPlus /> Add Program
                    </Button>
                  </div>
                </CardBody>
              </Card>
            </Col>

            {/* Users Card */}
            <Col md={4} className="mb-4">
              <Card className="text-center shadow border-0 bg-light">
                <CardBody>
                  <FaUsers size={50} className="text-danger mb-2" />
                  <CardTitle tag="h5" className="text-dark">Total Users</CardTitle>
                  <h3 className="text-danger font-weight-bold">{stats.users}</h3>
                  <div className="d-grid gap-2 mt-3">
                    <Link to="/admin/users" className="btn btn-outline-danger">Manage</Link>
                    <Button color="danger" tag={Link} to="/admin/users/add">
                      <FaPlus /> Add User
                    </Button>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          {/* Admin Guidelines Section */}
          <Card className="border-0 shadow-lg bg-white">
            <CardBody>
              <h4 className="text-center text-secondary"><FaExclamationCircle /> Admin Guidelines</h4>
              <ul className="mt-3 px-4">
                <li className="mb-2"><FaCheckCircle className="text-success" /> Use the "Manage" buttons to view and edit existing records.</li>
                <li className="mb-2"><FaCheckCircle className="text-success" /> Click "Add" to create new Universities, Programs, or Users.</li>
                <li className="mb-2"><FaCheckCircle className="text-success" /> Ensure all fields are filled correctly before adding data.</li>
                <li className="mb-2"><FaExclamationCircle className="text-danger" /> Deleting records is permanent. Proceed with caution.</li>
              </ul>
            </CardBody>
          </Card>
        </>
      )}
    </Container>
  );
};

export default AdminDashboard;
