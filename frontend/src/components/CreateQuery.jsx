import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoginGithub from "react-login-github";
import { AlertTitle, Alert } from "@mui/material/";

const CreateQuery = () => {
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();
  const [error, setError] = useState(false);

  const handleLogout = () => {
    // setUser({});
    // setUsername("");
    // setPassword("");
    localStorage.clear();
    setLogin(false);
    navigate("/");
    //  <a href="/dashboard">Dashboard</a>;
  };

  function submitQuery(e) {
    e.preventDefault();
    // Create the Post Request with the parameters
    let queryName = document.getElementById("queryName").value;
    let queryDescription = document.getElementById("queryDescription").value;
    let primaryKeyword = document.getElementById("primaryKeyword").value;
    let secondaryKeywords = document.getElementById("secondaryKeywords").value;

    //if one of the fields is blank, don't submit to database/don't let the submission work
    //need to figure out how to add pop up easily
    if (
      queryName == false ||
      queryDescription == false ||
      primaryKeyword == false ||
      secondaryKeywords == false
    ) {
      setError(true);
    } else {
      var data = {
        name: queryName,
        description: queryDescription,
        keywords: [primaryKeyword, secondaryKeywords],
      };

      fetch("http://127.0.0.1:8000/api/queries/", {
        //submitting a query
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
        body: JSON.stringify(data),
      });
      navigate("/queries/");
    }
    //  setError(false);
  }
  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      <div>
        <h1>401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
        your access, please return to the <a href="/">dashboard</a> to log in
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
    // alert("Please log in")
  } else {
    return (
      <div>
        <div id="page-wrapper">
          {/* <!-- Header --> */}
          <section id="header" className="wrapper">
            <button onClick={handleLogout}>Logout</button>
            {/* <!-- Logo --> */}
            <div id="logo">
              <h1>
                <a>SCOPE</a>
              </h1>
            </div>

            {/* <!-- Nav --> */}
            <nav id="nav">
              <ul>
                {/* <li><a href="left-sidebar.html">Left Sidebar</a></li> */}
                {/* <li><a href="right-sidebar.html">Right Sidebar</a></li> */}
                {/* <li><a href="no-sidebar.html">No Sidebar</a></li> */}
                <li className="current">
                  <a href="/">Dashboard</a>
                </li>
                <li>
                  <a href="/queries">Queries</a>
                </li>
                <li>
                  <a href="/results">Results</a>
                </li>
              </ul>
            </nav>
          </section>

          {/* <!-- Highlights --> */}
          <section id="highlights" className="wrapper style3">
            <div className="title">Create Query</div>
            <div className="container">
              <div className="form-style-5">
                <form>
                  <fieldset>
                    <legend> Query Info</legend>
                    <input
                      type="text"
                      id="queryName"
                      placeholder="Query Name *"
                    ></input>
                    <input
                      type="text"
                      id="queryDescription"
                      placeholder="Query Description (optional)"
                    ></input>
                    <input
                      type="text"
                      id="primaryKeyword"
                      placeholder="Primary Keyword (Only 1) *"
                    ></input>
                    <input
                      type="text"
                      id="secondaryKeywords"
                      placeholder="Secondary Keywords *"
                    ></input>
                  </fieldset>
                  <ul className="actions special">
                    <li>
                      <a onClick={submitQuery} className="button style1 large">
                        Submit Query
                      </a>
                    </li>
                    {error ? (
                     <Alert severity="error">Missing required fields</Alert>
                    ) : (
                      
                       <Alert severity="info">
                        Please fill in the above fields
                      </Alert>
                    )}
                  </ul>
                </form>
              </div>
            </div>
          </section>
        </div>

        {/* <!-- Scripts --> */}
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/jquery.dropotron.min.js"></script>
        <script src="assets/js/browser.min.js"></script>
        <script src="assets/js/breakpoints.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
      </div>
    );
  }
};

export default CreateQuery;
