import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoginGithub from "react-login-github";

const CreateQuery = () => {
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();

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

    var data = {
      name: queryName,
      description: queryDescription,
      keywords: [primaryKeyword, secondaryKeywords],
    };

    fetch("http://127.0.0.1:8000/api/queries/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });
    navigate("/queries");
  }

  return (
    <div>
      <div id="page-wrapper">
        {/* <GithubButton
            onClick={() => {

            }}
          /> */}

        <button onClick={handleLogout}>Logout</button>
        {/* <!-- Header --> */}
        <section id="header" className="wrapper">
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
                    placeholder="Query Description *"
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
};

export default CreateQuery;
