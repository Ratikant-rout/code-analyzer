import { useState } from "react";

function AnalyzeCode() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError("Please enter some code to analyze.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError(error.message || "Failed to analyze code");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-4xl font-bold text-blue-600 mb-6">Carbon Crunch</h1>

      <textarea
        className="w-full max-w-2xl h-40 p-3 border border-gray-300 rounded-md shadow-md focus:ring-2 focus:ring-blue-400"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter your code here..."
      />

      <button
        className={`bg-blue-500 text-white px-5 py-2 mt-4 rounded-md shadow-md transition ${
          loading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"
        }`}
        onClick={analyzeCode}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>

      {error && <p className="text-red-500 mt-3">{error}</p>}

      {result && (
        <div className="mt-6 p-5 bg-white shadow-lg rounded-md w-full max-w-2xl">
          {/* Overall Score with Progress Bar */}
          <h3 className="text-xl font-semibold text-green-600">
            Overall Score: {result.overall_score} / 100
          </h3>
          <div className="w-full bg-gray-200 rounded-full h-4 mt-2">
            <div
              className="bg-green-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${result.overall_score}%` }}
            ></div>
          </div>

          {/* Breakdown Scores in a Grid */}
          <h4 className="mt-4 text-lg font-medium">Breakdown:</h4>
          <div className="grid grid-cols-2 gap-3 mt-2">
            {Object.entries(result.breakdown).map(([key, value]) => (
              <div key={key} className="p-3 bg-gray-100 rounded-md shadow-sm">
                <span className="font-semibold text-blue-600 capitalize">
                  {key}:
                </span>{" "}
                <span className="text-gray-700">{value}</span>
              </div>
            ))}
          </div>

          {/* Recommendations as a List */}
          <h4 className="mt-5 text-lg font-medium">Recommendations:</h4>
          <ul className="mt-2 space-y-2">
            {result.recommendations.map((rec, index) => (
              <li
                key={index}
                className="p-3 bg-yellow-100 border-l-4 border-yellow-500 rounded-md shadow-sm"
              >
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default AnalyzeCode;

