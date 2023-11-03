import React, { useState, useEffect } from "react";
import "../assets/css/dashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";
import LoginGithub from "react-login-github";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import stars from "./../images/stars3.jpg";
import create from "./../images/icons/create_queries.png";
import filter from "./../images/icons/filtering_queries.png";
import workspaces from "./../images/icons/workspaces.png";

import ScopeNavBar from "./ScopeNavBar";
const Dashboard = () => {
  return (
    <div>
      <div
        style={{
          backgroundImage: `url(${stars})`,
          // height: '24em',
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }}
      >
        <h1 className="header">
          <img src={logo} width="100" height="100" alt="Scope logo" /> SCOPE
        </h1>
      </div>
      <h2 className="headings">What is SCOPE?</h2>
      <p className="paragraphs">
        Formerly an acronym for "Scientific Collection of Policy Evidence,"
        SCOPE is a tool that enhances the experience of the geoLab researchers
        by giving them automated summaries and key words of news articles from
        A.I. models, creating controllable search queries, and collaborating on
        workspaces. Researchers may submit queries on any topic of interest,
        such as international relations or environmental development projects.
        They may submit them with keywords, receive A.I.-enhanced results for
        them, and filter through them on a results page. The Workspaces
        component of SCOPE serves as a way for people to make and share
        collections of articles gathered from queries and group them by specific
        category or project task.
      </p>
      <div></div>
      <h2 className="headings">How to use SCOPE</h2>

      <h3 className="headings2">
        {" "}
        <img src={create} width="50" height="50" alt="create" /> &nbsp; Creating
        Queries
      </h3>
      <p className="paragraphs">
        To see and create queries, you'll need to log in with your github
        account. After you log in, you will be able to see all the queries you
        have made in the past and you can create new queries by clicking the
        create query button. You will need to give the query a title,
        description, and keywords. You can only enter one primary keyword, but
        you can enter multiple secondary keywords. The keywords will be used to
        generate relevant sources that you can see by clicking on the title of
        the query. To search through your queries, you can change the dropdown
        near the search bar to search either by name, description, or keywords.
      </p>

      <p className="paragraphs_end"></p>

      <h3 className="headings2">
        {" "}
        <img src={filter} width="50" height="50" alt="filter" /> &nbsp;
        Filtering Results
      </h3>
      <p className="paragraphs">
        By clicking on a query's title, you can see the list of sources relevant
        to the query. The sources will be displayed in order by relevance (to
        the keywords), but you can also filter the sources by article title,
        date (when the source was added to our database), location, and
        language.
      </p>

      <p className="paragraphs_end"></p>

      <h3 className="headings2">
        {" "}
        <img src={workspaces} width="50" height="50" alt="workspaces" /> &nbsp;
        Using Workspaces
      </h3>

      <p className="paragraphs_end">
        As stated above, workspaces are collaborative spaces for users to be
        able to add sources relevant to a specific project they're working on.
        In the workspaces tab, you can either join an existing workspace (if you
        have the name and password) or create a new workspace (where you will
        give it a name and password). To share it with other people, they will
        just need the name and password to join. You are able to join and create
        multiple workspaces. You are also able to add tags to a workspace to
        group workspaces by topic or project.
      </p>

      <div className="footnote">William & Mary geoDev</div>
    </div>
  );
};

export default Dashboard;
