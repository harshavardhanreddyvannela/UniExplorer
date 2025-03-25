import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Container, Row, Col, Card, CardBody, CardTitle } from "reactstrap";

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    universities: 0,
    programs: 0,
    users: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const uniRes = await axios.get("http://localhost:6969/api/universities");
        const progRes = await axios.get("http://localhost:6969/api/programs");
        const userRes = await axios.get("http://localhost:6969/api/user");

        setStats({
          universities: uniRes.data.total,
          programs: progRes.data.total,
          users: userRes.data.total,
        });
      } catch (error) {
        console.error("Error fetching stats:", error);
      }
    };
    fetchStats();
  }, []);

  return (
    <Container>
      <h2 className="my-4">Admin Dashboard</h2>
      <Row>
        <Col md={4}>
          <Card className="text-center">
            <CardBody>
              <CardTitle tag="h5">Total Universities</CardTitle>
              <h3>{stats.universities}</h3>
              <Link to="/admin/universities" className="btn btn-primary">Manage</Link>
            </CardBody>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center">
            <CardBody>
              <CardTitle tag="h5">Total Programs</CardTitle>
              <h3>{stats.programs}</h3>
              <Link to="/admin/programs" className="btn btn-primary">Manage</Link>
            </CardBody>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="text-center">
            <CardBody>
              <CardTitle tag="h5">Total Users</CardTitle>
              <h3>{stats.users}</h3>
              <Link to="/admin/users" className="btn btn-primary">Manage</Link>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default AdminDashboard;
