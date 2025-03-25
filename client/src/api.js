const API_BASE_URL = "http://localhost:6969/api";

export const fetchUniversities = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/universities`);
    const data = await response.json();
    return data.universities;
  } catch (error) {
    console.error("Error fetching universities:", error);
    return [];
  }
};