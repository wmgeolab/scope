import React, { useState, useEffect } from "react";
import Link from 'react-dom';
import {BrowserRouter, Routes, Route, useNavigate, Navigate} from "react-router-dom";
import './App.css';
import LoginGithub from 'react-login-github';

import Login from "./components/Login"; //  can have code here or on different component
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";
import CreateQuery from "./components/CreateQuery";

function App() {

  return (
    <BrowserRouter>
      {/* <Router> */}
      <div className="App">
      </div>
        <Routes>
          {/* this makes it so I can't go to any of the routes without logging in */}
           {/* <Route path="/dashboard" render={() => <Dashboard />}/>  */}
            {/* <Route element={<Login />}>    */}
             <Route exact path="/" element={<Dashboard />} />
            <Route exact path="/queries" element={<Queries />} />
            <Route exact path="/results" element={<Results />} />
            <Route exact path="/create-query" element={<CreateQuery />} />
         {/* </Route>  */}
        </Routes>
      {/* </Router> */}
    </BrowserRouter>
  );
}

export default App;
