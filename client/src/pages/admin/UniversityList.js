import React, { useEffect, useState } from "react";
import axios from "axios";
import { Table, Button, Container } from "reactstrap";

const UniversityList = () => {
  const [universities, setUniversities] = useState([]);

  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const res = await axios.get("http://localhost:6969/api/universities");
        setUniversities(res.data.universities);
      } catch (error) {
        console.error("Error fetching universities:", error);
      }
    };
    fetchUniversities();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/universities/${id}`);
      setUniversities(universities.filter((uni) => uni._id !== id));
    } catch (error) {
      console.error("Error deleting university:", error);
    }
  };

  return (
    <Container>
      <h2 className="my-4">Manage Universities</h2>
      <Table bordered>
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Ranking</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {universities.map((uni) => (
            <tr key={uni._id}>
              <td>{uni.name}</td>
              <td>{uni.location}</td>
              <td>{uni.ranking}</td>
              <td>
                <Button color="danger" onClick={() => handleDelete(uni._id)}>
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default UniversityList;
