import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import "bootstrap/dist/css/bootstrap.min.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Web vitals monitoring
if (process.env.NODE_ENV === 'production') {
  reportWebVitals(console.log); // Log web vitals in production
} else {
  // In development, you can skip logging or send it elsewhere
  reportWebVitals();
}

