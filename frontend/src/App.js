import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import './App.css';
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";
import Workspaces from "./components/Workspaces";
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
            <Route exact path="/workspaces" element={<Workspaces />} /> 
            <Route exact path="/queries/" element={<Queries />} />
            <Route path="/results/:query_id/" element={<Results />} />
            <Route exact path="/create-query" element={<CreateQuery />} />
         {/* </Route>  */}
        </Routes>
      {/* </Router> */}
    </BrowserRouter>
  );
}

export default App;
