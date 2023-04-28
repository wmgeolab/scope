import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import './App.css';
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";
import CreateQuery from "./components/CreateQuery";
import DisplayArticle from "./components/DisplayArticle";
import Workspaces from "./components/Workspaces";
import Individual_Workspaces from "./components/individualWorkspacePage";

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
            <Route exact path="/queries" element={<Queries />} />
            <Route path="/results/:query_id" element={<Results />} />
            <Route exact path="/display-article/:article_title" element={<DisplayArticle />} />
            <Route path="/workspaces" element={<Workspaces />} />
            <Route path="/workspace/:workspace_name" element={<Individual_Workspaces />} />
            <Route exact path="/create-query" element={<CreateQuery />} />
         {/* </Route>  */}
        </Routes>
      {/* </Router> */}
    </BrowserRouter>
  );
}

export default App;
