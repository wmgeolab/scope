import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Router, Routes, Route, Navigate} from "react-router-dom";
import './App.css';

import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";

function App() {
  return (
    <div className="App">
      <h2>SCOPE</h2>

    <BrowserRouter>
      {/* <Router> */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/queries" element={<Queries />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      {/* </Router> */}
    </BrowserRouter>
    </div>
  );
}

export default App;
