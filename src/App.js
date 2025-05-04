import { useState, useEffect } from "react";
import AnalyzeCode from "./AnalyzeCode";
import "bootstrap/dist/css/bootstrap.min.css"; // ✅ Ensure Bootstrap is imported

function App() {
  // 🌙 Dark mode state
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("theme") === "dark"
  );

  // ✅ Log when button is clicked
  const toggleDarkMode = () => {
    console.log("Button Clicked! Current dark mode:", darkMode);
    setDarkMode(!darkMode);
  };

  // ✅ Log when theme changes
  useEffect(() => {
    console.log("Dark Mode State Changed:", darkMode);

    if (darkMode) {
      document.body.classList.add("bg-dark", "text-light");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("bg-dark", "text-light");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  return (
    <div className="container d-flex flex-column align-items-center justify-content-center min-vh-100">
      {/* ✅ Bootstrap Dark Mode Toggle Button */}
      <button onClick={toggleDarkMode} className="btn btn-primary mb-4">
        {darkMode ? "Switch to Light Mode ☀️" : "Switch to Dark Mode 🌙"}
      </button>

      {/* ✅ Bootstrap Card */}
      <div className="card shadow-lg p-4 w-75">
        <AnalyzeCode />
      </div>
    </div>
  );
}

export default App;


