import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Container,
  Card,
  CardBody,
  CardTitle,
  CardText,
  ListGroup,
  ListGroupItem,
  Button,
  Spinner,
} from "reactstrap";

const UniversityDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUniversityDetails();
  }, []);

  const fetchUniversityDetails = async () => {
    try {
      const response = await fetch(`http://localhost:6969/api/universities/${id}`);
      const data = await response.json();
      setUniversity(data);
    } catch (error) {
      console.error("Error fetching university details:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return (
      <Container className="mt-5 text-center">
        <Spinner color="primary" />
        <h4 className="mt-3">Fetching university details...</h4>
      </Container>
    );

  if (!university)
    return <h2 className="text-center mt-5 text-danger">University not found</h2>;

  return (
    <Container className="mt-5 d-flex justify-content-center">
      <Card className="shadow-lg p-4" style={{ maxWidth: "700px", width: "100%" }}>
        <CardBody className="text-center">
          <CardTitle tag="h2" className="mb-3 text-primary">
            {university.name}
          </CardTitle>
          <CardText>
            <strong>📍 Location:</strong> {university.location}
          </CardText>
          <CardText>
            <strong>🏆 Ranking:</strong> {university.ranking}
          </CardText>
          <CardText className="text-muted">{university.description}</CardText>

          {/* Visit Website Button */}
          <a
            href={university.website}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-info btn-lg my-3"
          >
            🌐 Visit Website
          </a>

          {/* Display Programs */}
          <h4 className="mt-4">🎓 Programs Offered:</h4>
          {university.programs && university.programs.length > 0 ? (
            <ListGroup className="mb-3">
              {university.programs.map((program, index) => (
                <ListGroupItem key={index} className="text-left">
                  {program}
                </ListGroupItem>
              ))}
            </ListGroup>
          ) : (
            <p className="text-muted">No programs listed.</p>
          )}

          {/* Back Button */}
          <Button
            color="secondary"
            size="lg"
            className="mt-3"
            onClick={() => navigate("/universities")}
          >
            🔙 Back to Universities
          </Button>
        </CardBody>
      </Card>
    </Container>
  );
};

export default UniversityDetails;
