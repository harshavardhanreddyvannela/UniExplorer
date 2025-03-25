import React from "react";
import { useNavigate } from "react-router-dom";
import { Container, Button, Row, Col, Card, CardBody, CardTitle, CardText } from "reactstrap";

const rankingsData = [
  {
    title: "Global Rankings",
    icon: "🌍",
    rankings: [
      { name: "QS World Ranking", url: "https://www.topuniversities.com/qs-world-university-rankings", color: "warning" },
      { name: "THE World Ranking", url: "https://www.timeshighereducation.com/world-university-rankings", color: "info" },
      { name: "US News Global Ranking", url: "https://www.usnews.com/education/best-global-universities/rankings", color: "primary" },
    ],
  },
  {
    title: "USA Rankings",
    icon: "🇺🇸",
    rankings: [
      { name: "US News College Ranking", url: "https://www.usnews.com/best-colleges", color: "danger" },
      { name: "NCAA Leaderboard", url: "https://www.ncaa.com/rankings", color: "success" },
      { name: "Forbes Top Colleges", url: "https://www.forbes.com/top-colleges/", color: "info" },
    ],
  },
  {
    title: "UK Rankings",
    icon: "🇬🇧",
    rankings: [
      { name: "The Complete University Guide", url: "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings", color: "secondary" },
      { name: "The Guardian University Guide", url: "https://www.theguardian.com/education/universityguide", color: "dark" },
      { name: "THE UK Rankings", url: "https://www.timeshighereducation.com/student/best-universities/best-universities-uk", color: "danger" },
    ],
  },
  {
    title: "Australia Rankings",
    icon: "🇦🇺",
    rankings: [
      { name: "QS Australia Ranking", url: "https://www.topuniversities.com/qs-world-university-rankings/australia", color: "warning" },
      { name: "THE Australia Ranking", url: "https://www.timeshighereducation.com/world-university-rankings/2023/subject-ranking/australia", color: "info" },
      { name: "Good Universities Guide", url: "https://www.gooduniversitiesguide.com.au/rankings", color: "primary" },
    ],
  },
  {
    title: "India Rankings",
    icon: "🇮🇳",
    rankings: [
      { name: "NIRF India Ranking", url: "https://www.nirfindia.org/2023/Ranking", color: "danger" },
      { name: "Outlook India Ranking", url: "https://www.outlookindia.com/education/best-universities-in-india", color: "success" },
      { name: "THE India Ranking", url: "https://www.timeshighereducation.com/world-university-rankings/india", color: "info" },
    ],
  },
  {
    title: "Canada Rankings",
    icon: "🇨🇦",
    rankings: [
      { name: "QS Canada Ranking", url: "https://www.topuniversities.com/qs-world-university-rankings/canada", color: "warning" },
      { name: "Maclean’s University Ranking", url: "https://www.macleans.ca/education/university-rankings/", color: "info" },
      { name: "THE Canada Ranking", url: "https://www.timeshighereducation.com/world-university-rankings/canada", color: "primary" },
    ],
  },
];

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container className="mt-5 text-center">
      {/* Hero Section */}
      <div className="p-5 bg-primary text-white rounded hero-section">
        <h1 className="display-4">Welcome to University Explorer!</h1>
        <p className="lead">
          Your gateway to discovering top universities, their rankings, and programs worldwide.
        </p>
        <Button color="light" className="mt-3" onClick={() => navigate("/universities")}>
          Explore Universities
        </Button>
      </div>

      {/* Features Section */}
      <Row className="mt-5">
        <Col md={4}>
          <Card className="shadow feature-card">
            <CardBody>
              <CardTitle tag="h4">Top-Ranked Universities</CardTitle>
              <CardText>Browse the best universities based on global rankings.</CardText>
            </CardBody>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="shadow feature-card">
            <CardBody>
              <CardTitle tag="h4">Diverse Programs</CardTitle>
              <CardText>Find programs that match your interests and career goals.</CardText>
            </CardBody>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="shadow feature-card">
            <CardBody>
              <CardTitle tag="h4">Comprehensive Details</CardTitle>
              <CardText>Get insights on tuition fees, location, and university facilities.</CardText>
            </CardBody>
          </Card>
        </Col>
      </Row>

      {/* Rankings Section */}
      <div className="mt-5">
        <h3 className="mb-4">✈️Explore University Rankings</h3>
        <Row>
          {rankingsData.map((rankingCategory, index) => (
            <Col md={4} key={index} className="mb-4">
              <Card className="shadow ranking-card">
                <CardBody>
                  <div className="icon-container" style={{ fontSize: "30px" }}>{rankingCategory.icon}</div>
                  <CardTitle tag="h4">{rankingCategory.title}</CardTitle>
                  {rankingCategory.rankings.map((ranking, idx) => (
                    <Button
                      key={idx}
                      color={ranking.color}
                      block
                      className="mb-2"
                      onClick={() => window.open(ranking.url, "_blank")}
                    >
                      {ranking.name}
                    </Button>
                  ))}
                </CardBody>
              </Card>
            </Col>
          ))}
        </Row>
      </div>
    </Container>
  );
};

export default Home;
