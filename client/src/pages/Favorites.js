import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Row, Col, Card, CardBody, CardTitle, Button, Spinner, Alert } from "reactstrap";
import { FaHeartBroken } from "react-icons/fa";

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFavorites = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("You need to be logged in to view favorites.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get("http://localhost:6969/api/user/favorites", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setFavorites(response.data);
      } catch (error) {
        console.error("Error fetching favorites:", error);
        setError("Failed to load favorites. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  const toggleFavorite = async (universityId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in!");
      return;
    }

    try {
      await axios.delete(`http://localhost:6969/api/user/favorites/${universityId}`, {
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

  if (loading) {
    return (
      <Container className="text-center mt-5">
        <Spinner color="primary" />
        <p>Loading favorites...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert color="danger">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-primary text-center">Your Favorite Universities</h2>

      {favorites.length === 0 ? (
        <div className="text-center mt-5">
          <FaHeartBroken size={60} color="gray" />
          <h4 className="mt-3 text-muted">No favorites added yet</h4>
          <p className="text-muted">Start adding universities to your favorites list!</p>
        </div>
      ) : (
        <Row>
          {favorites.map((university) => (
            <Col md={4} key={university._id}>
              <Card className="mb-4 shadow-sm">
                <CardBody className="text-center">
                  <CardTitle tag="h5" className="text-dark">{university.name}</CardTitle>
                  <p className="text-muted">{university.location || "Unknown Location"}</p>
                  <Button color="danger" outline onClick={() => toggleFavorite(university._id)}>
                    Remove from Favorites
                  </Button>
                </CardBody>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default Favorites;
