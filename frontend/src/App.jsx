import React, { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Dashboard from "./components/Dashboard";
import Queries from "./components/queries/Queries";
import Results from "./components/queries/Results";
import Workspaces from "./components/workspaces/Workspaces";
import CreateQuery from "./components/queries/CreateQuery";
import DisplayArticle from "./components/queries/DisplayArticle";
import ScopeNavBar from "./components/ScopeNavBar";
import IndividualWorkspaces from "./components/workspaces/individual_workspaces/IndividualWorkspacePage";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div className="App">
      <BrowserRouter>
        <ScopeNavBar loggedIn={loggedIn} setLoggedIn={setLoggedIn} />
        <Routes>
          <Route exact path="/" element={<Dashboard />} />
          <Route
            exact
            path="/workspaces"
            element={<Workspaces loggedIn={loggedIn} />}
          />
          <Route
            exact
            path="/queries"
            element={<Queries loggedIn={loggedIn} />}
          />
          <Route
            path="/results/:query_id"
            element={<Results loggedIn={loggedIn} />}
          />
          <Route
            exact
            path="/display-article/:article_title"
            element={<DisplayArticle />}
          />
          <Route path="/workspaces" element={<Workspaces />} />
          <Route
            path="/workspace/:workspace_name/id/:workspace_id"
            element={<IndividualWorkspaces />}
          />
          <Route exact path="/create-query" element={<CreateQuery />} />
        </Routes>
      </BrowserRouter>
      <div></div>
    </div>
  );
}

export default App;