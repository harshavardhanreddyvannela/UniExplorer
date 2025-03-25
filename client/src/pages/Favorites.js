import React, { useEffect, useState } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  CardBody,
  CardTitle,
  CardText,
  Button,
} from "reactstrap";
import axios from "axios";

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await axios.get("http://localhost:6969/api/user/favorites", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setFavorites(response.data);
    } catch (error) {
      console.error("Error fetching favorites:", error);
    }
  };

  const toggleFavorite = async (universityId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in!");
      return;
    }

    const url = `http://localhost:6969/api/user/favorites/${universityId}`;

    try {
      await axios.delete(url, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Smoothly remove the university from the list
      setFavorites((prevFavorites) =>
        prevFavorites.filter((fav) => fav._id !== universityId)
      );
    } catch (error) {
      console.error("Error removing from favorites:", error.response?.data || error);
    }
  };

  return (
    <Container className="mt-4">
      <h1 className="text-center mb-4 text-primary">⭐ My Favorite Universities</h1>
      <Row className="justify-content-center">
        {favorites.length === 0 ? (
          <h4 className="text-center w-100 text-muted">No favorite universities found</h4>
        ) : (
          favorites.map((uni) => (
            <Col md={6} lg={4} key={uni._id} className="mb-4">
              <Card className="shadow-sm border-0 rounded hover-effect">
                <div className="card-image">
                  <img
                    src={uni.image || "https://via.placeholder.com/400x200?text=University"}
                    alt={uni.name}
                    className="img-fluid rounded-top"
                  />
                </div>
                <CardBody>
                  <CardTitle tag="h5" className="text-dark font-weight-bold">
                    {uni.name}
                  </CardTitle>
                  <CardText className="text-muted">{uni.location}</CardText>
                  <CardText>
                    <strong>Ranking:</strong> {uni.ranking || "N/A"}
                  </CardText>
                  <div className="d-flex justify-content-between">
                    <Button
                      color="danger"
                      onClick={() => toggleFavorite(uni._id)}
                      className="btn-sm"
                    >
                      ❌ Remove
                    </Button>
                    {uni.website && (
                      <Button
                        color="primary"
                        className="btn-sm"
                        href={uni.website}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        🌐 Visit
                      </Button>
                    )}
                  </div>
                </CardBody>
              </Card>
            </Col>
          ))
        )}
      </Row>
    </Container>
  );
};

export default Favorites;
