import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Row, Col, Card, CardBody, CardTitle, Button } from "reactstrap";

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    const fetchFavorites = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found");
        return;
      }

      try {
        const response = await axios.get("http://localhost:6969/api/user/favorites", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setFavorites(response.data);
      } catch (error) {
        console.error("Error fetching favorites:", error);
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
    <Container>
      <h2 className="my-4">Favorites</h2>
      <Row>
        {favorites.map((university) => (
          <Col md={4} key={university._id}>
            <Card className="mb-4">
              <CardBody>
                <CardTitle tag="h5">{university.name}</CardTitle>
                <Button color="danger" onClick={() => toggleFavorite(university._id)}>
                  Remove from Favorites
                </Button>
              </CardBody>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Favorites;