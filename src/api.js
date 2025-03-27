import axios from "axios";

// ✅ Update API URL for deployment
const API_URL = "https://code-analyzer-wkyt.onrender.com"; // Replace with actual backend URL

// ✅ Check API status
export const getStatus = async () => {
  try {
    const response = await axios.get(`${API_URL}/`);
    return response.data;
  } catch (error) {
    console.error(
      "Error fetching API status:",
      error.response?.data || error.message
    );
    return null;
  }
};

// ✅ Analyze code function
export const analyzeCode = async (code) => {
  try {
    const response = await axios.post(
      `${API_URL}/analyze`,
      { code }, // Sending code as JSON body
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  } catch (error) {
    console.error(
      "Error analyzing code:",
      error.response?.data || error.message
    );
    return null;
  }
};




