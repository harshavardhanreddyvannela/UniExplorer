import React, { useEffect, useState } from "react";
import axios from "axios";
import { Table, Button, Container } from "reactstrap";

const ProgramList = () => {
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        const res = await axios.get("http://localhost:6969/api/programs");
        setPrograms(res.data.programs);
      } catch (error) {
        console.error("Error fetching programs:", error);
      }
    };
    fetchPrograms();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/programs/${id}`);
      setPrograms(programs.filter((prog) => prog._id !== id));
    } catch (error) {
      console.error("Error deleting program:", error);
    }
  };

  return (
    <Container>
      <h2 className="my-4">Manage Programs</h2>
      <Table bordered>
        <thead>
          <tr>
            <th>Name</th>
            <th>Duration</th>
            <th>Degree Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {programs.map((prog) => (
            <tr key={prog._id}>
              <td>{prog.name}</td>
              <td>{prog.duration}</td>
              <td>{prog.degreeType}</td>
              <td>
                <Button color="danger" onClick={() => handleDelete(prog._id)}>
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

export default ProgramList;
