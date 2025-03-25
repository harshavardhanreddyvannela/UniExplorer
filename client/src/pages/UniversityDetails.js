import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Row, Col, Card, CardBody, CardTitle, Button } from "reactstrap";

const UniversityDetails = ({ match }) => {
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUniversityDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:6969/api/universities/${match.params.id}`);
        setUniversity(response.data);
      } catch (error) {
        console.error("Error fetching university details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUniversityDetails();
  }, [match.params.id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!university) {
    return <div>University not found</div>;
  }

  return (
    <Container>
      <h2 className="my-4">{university.name}</h2>
      <Row>
        <Col md={12}>
          <Card className="mb-4">
            <CardBody>
              <CardTitle tag="h5">Programs</CardTitle>
              <ul>
                {university.programs.map((program) => (
                  <li key={program._id}>{program.name}</li>
                ))}
              </ul>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default UniversityDetails;