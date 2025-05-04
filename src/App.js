import { useState, useEffect } from "react";
import AnalyzeCode from "./AnalyzeCode";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("theme") === "dark"
  );
  const [analysisResult, setAnalysisResult] = useState(null);  // To store the analysis results

  const toggleDarkMode = () => {
    console.log("Button Clicked! Current dark mode:", darkMode);
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    console.log("Dark Mode State Changed:", darkMode);

    if (darkMode) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  // This function will be passed down to AnalyzeCode to update the parent component's state
  const handleAnalysisResult = (result) => {
    setAnalysisResult(result);
  };

  return (
    <div className="container d-flex flex-column align-items-center justify-content-center min-vh-100">
      <button onClick={toggleDarkMode} className="btn btn-primary mb-4">
        {darkMode ? "Switch to Light Mode ☀️" : "Switch to Dark Mode 🌙"}
      </button>

      <div className="card shadow-lg p-4 w-75">
        <AnalyzeCode onAnalyzeComplete={handleAnalysisResult} />
      </div>

      {/* Feedback Section */}
      {analysisResult && (
        <div className="feedback-container mt-4">
          <h3>Overall Score: {analysisResult.overall_score} / 100</h3>
          <p>📊 Breakdown:</p>
          <ul>
            {Object.entries(analysisResult.breakdown).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {value}
              </li>
            ))}
          </ul>
          <p>✅ Recommendations:</p>
          <ul>
            {analysisResult.recommendations.slice(0, 3).map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
            {analysisResult.recommendations.length === 0 && (
              <li>No recommendations available.</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;


