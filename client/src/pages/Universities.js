import React, { useEffect, useState } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  CardBody,
  CardTitle,
  CardText,
  Input,
  Button,
  Spinner,
} from "reactstrap";
import { Link } from "react-router-dom";
import axios from "axios";
import { FaHeart, FaRegHeart, FaSort } from "react-icons/fa"; // Import icons

const Universities = () => {
  const [universities, setUniversities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [program, setProgram] = useState("");
  const [sortBy, setSortBy] = useState("ranking");
  const [order, setOrder] = useState("asc");
  const [favorites, setFavorites] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchUniversities();
      if (token) fetchFavorites();
    }, 500);

    return () => clearTimeout(delayDebounce);
  }, [search, location, program, sortBy, order]);

  const fetchUniversities = async () => {
    setLoading(true);
    try {
      let url = `http://localhost:6969/api/universities?sortBy=${sortBy}&order=${order}`;
      if (search) url += `&name=${search}`;
      if (location) url += `&location=${location}`;
      if (program) url += `&program=${program}`;
  
      const response = await fetch(url);
      const data = await response.json();
      
      setUniversities(Array.isArray(data.universities) ? data.universities : []);
    } catch (error) {
      console.error("Error fetching universities:", error);
      setUniversities([]); // Fallback to empty array
    } finally {
      setLoading(false);
    }
  };

  const fetchFavorites = async () => {
    try {
      const response = await axios.get("http://localhost:6969/api/user/favorites", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setFavorites(response.data.map((fav) => fav._id));
    } catch (error) {
      console.error("Error fetching favorites:", error);
    }
  };

  const handleFavorite = async (universityId) => {
    if (!token) {
      alert("You must be logged in to add favorites!");
      return;
    }

    try {
      if (favorites.includes(universityId)) {
        await axios.delete(`http://localhost:6969/api/user/favorites/${universityId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setFavorites(favorites.filter((id) => id !== universityId));
      } else {
        await axios.post(`http://localhost:6969/api/user/favorites/${universityId}`, {}, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setFavorites([...favorites, universityId]);
      }
    } catch (error) {
      console.error("Error updating favorites:", error);
    }
  };

  return (
    <Container className="mt-4">
      <h1 className="text-center mb-4 text-primary">🎓 Explore Universities</h1>
      
      {/* Search & Filter Section */}
      <Row className="mb-4 g-2">
        <Col md={4}>
          <Input
            type="text"
            placeholder="🔍 Search by name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="rounded-pill"
          />
        </Col>
        <Col md={4}>
          <Input
            type="text"
            placeholder="📍 Filter by location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="rounded-pill"
          />
        </Col>
        <Col md={3}>
          <Input
            type="text"
            placeholder="🎓 Filter by program"
            value={program}
            onChange={(e) => setProgram(e.target.value)}
            className="rounded-pill"
          />
        </Col>
        <Col md={2}>
          <Input
            type="select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="rounded-pill"
          >
            <option value="ranking">🏆 Ranking</option>
            <option value="name">🔠 Name</option>
          </Input>
        </Col>
        <Col md={2}>
  <Button
    color="dark"
    className="rounded-pill"
    onClick={() => setOrder(order === "asc" ? "desc" : "asc")}
  >
    <FaSort /> {order === "asc" ? "Ascending" : "Descending"}
  </Button>
</Col>

      </Row>

      {/* Loading & Results */}
      {loading ? (
        <div className="text-center">
          <Spinner color="primary" />
          <p>Fetching universities...</p>
        </div>
      ) : universities.length === 0 ? (
        <h4 className="text-center text-muted">No universities found</h4>
      ) : (
        <Row>
          {universities.map((uni) => (
            <Col md={4} key={uni._id} className="mb-4">
              <Card className="shadow-sm border-0 hover-effect">
              <CardBody className="d-flex flex-column justify-content-between position-relative">
  {/* Favorite Button - Positioned at the Top-Right */}
  <Button
    color="link"
    className="position-absolute top-0 end-0 m-2 p-2"
    onClick={() => handleFavorite(uni._id)}
  >
    {favorites.includes(uni._id) ? (
      <FaHeart size={20} color="red" />
    ) : (
      <FaRegHeart size={20} color="gray" />
    )}
  </Button>

  {/* University Info */}
  <div className="text-center mt-2">
    <CardTitle tag="h5" className="text-primary">
      {uni.name}
    </CardTitle>
    <CardText className="text-muted">
      <strong>📍 Location:</strong> {uni.location}
    </CardText>
    <CardText>
      <strong>🏆 Ranking:</strong> {uni.ranking}
    </CardText>
  </div>

  {/* Buttons Row - Positioned at the Bottom */}
  <div className="d-flex justify-content-between mt-3">
    <a
      href={uni.website}
      target="_blank"
      rel="noopener noreferrer"
      className="btn btn-outline-info btn-sm"
    >
      🌐 Visit Website
    </a>
    <Link to={`/universities/${uni._id}`}>
      <Button color="primary" size="sm">
        ℹ️ View Details
      </Button>
    </Link>
  </div>
</CardBody>

              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default Universities;
