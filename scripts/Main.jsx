import React from "react";
import ReactDOM from "react-dom";

import App from "./app";

const rootElement = document.getElementById("content");
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  rootElement
);
