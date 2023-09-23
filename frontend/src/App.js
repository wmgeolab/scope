import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";
import Workspaces from "./components/Workspaces";
import CreateQuery from "./components/CreateQuery";
import DisplayArticle from "./components/DisplayArticle";
import IndividualWorkspaces from "./components/individualWorkspacePage";
import QuestionSettings from "./components/QuestionSettings";

function App() {
  return (
    <BrowserRouter>
      <div className="App"></div>
      <Routes>
        <Route exact path="/" element={<Dashboard />} />
        <Route exact path="/workspaces" element={<Workspaces />} />
        <Route exact path="/queries" element={<Queries />} />
        <Route path="/results/:query_id" element={<Results />} />
        <Route path="/question_settings" element={<QuestionSettings />} />
        <Route
          exact
          path="/display-article/:article_title"
          element={<DisplayArticle />}
        />
        <Route path="/workspaces" element={<Workspaces />} />
        <Route
          path="/workspace/:workspace_name"
          element={<IndividualWorkspaces />}
        />
        <Route exact path="/create-query" element={<CreateQuery />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
