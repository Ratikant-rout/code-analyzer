import { useState } from "react";

function AnalyzeCode() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);

  const analyzeCode = async () => {
    try {
      console.log("Sending request to backend...");
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (!response.ok)
        throw new Error(`Failed to analyze code: ${response.status}`);

      const data = await response.json();
      console.log("Response from backend:", data);
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to analyze code. Check console for details.");
    }
  };

  return (
    <div>
      <h1>Carbon Crunch</h1>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter your code here..."
        rows={8}
        cols={50}
      />
      <button onClick={analyzeCode}>Analyze Code</button>

      {result && (
        <div>
          <h3>Overall Score: {result.overall_score}</h3>
          <h4>Breakdown:</h4>
          <ul>
            {Object.entries(result.breakdown).map(([key, value]) => (
              <li key={key}>
                {key}: {value}
              </li>
            ))}
          </ul>
          <h4>Recommendations:</h4>
          <ul>
            {result.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default AnalyzeCode;
