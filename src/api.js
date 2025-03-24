import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // FastAPI backend

export const getStatus = async () => {
  try {
    const response = await axios.get(`${API_URL}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching status:", error);
    return null;
  }
};

export const analyzeCode = async () => {
  try {
    const response = await axios.get(`${API_URL}/analyze`);
    return response.data;
  } catch (error) {
    console.error("Error analyzing code:", error);
    return null;
  }
};
