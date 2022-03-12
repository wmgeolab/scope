import React from 'react';
import Link from 'react-dom';
import {BrowserRouter, Router, Routes, Route, Navigate} from "react-router-dom";
import './App.css';

import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";

function App() {
  return (
    
      
    <BrowserRouter>
      {/* <Router> */}
      <div className="App">
      <h2>SCOPE</h2>
      </div>
        <Routes>
          <Route path="/" element={<Login />} />
          {/* this makes it so I can't go to any of the routes without logging in */}
           <Route element={<Login />}>   
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/queries" element={<Queries />} />
            <Route path="/results" element={<Results />} />
          </Route>  
        </Routes>
      {/* </Router> */}
    </BrowserRouter>


    
  );
}

export default App;
