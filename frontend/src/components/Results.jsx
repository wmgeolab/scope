import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Route, useNavigate } from "react-router-dom";
import Dashboard from "./Dashboard";
const Queries = () => {
  const [queries, setQueries] = useState([]);
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/queries/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    let q = await response.json();

    console.log(q);
    setQueries(q.results);

    return q;
  };

  useEffect(() => {
    handleSubmit();
  }, []); //listening on an empty array

  const handleLogout = () => {
    // setUser({});
    // setUsername("");
    // setPassword("");
    localStorage.clear();
    setLogin(false);
    navigate("/");
    //  <a href="/dashboard">Dashboard</a>;
  };

  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      <div>
        You are not logged in, please return to the <a href="/">dashboard</a>{" "}
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
    // alert("Please log in")
  } else {
    return (
      <div>
        <button onClick={handleLogout}>Logout</button>
        <title>SCOPE</title>
        <meta charSet="utf-8" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, user-scalable=no"
        />
        <link rel="stylesheet" href="assets/css/table.css" />
        <link rel="stylesheet" href="assets/css/main.css" />
        <div id="page-wrapper">
          {/* <!-- Header --> */}
          <section id="header" className="wrapper">
            {/* <!-- Logo --> */}
            <div id="logo">
              <h1>
                <a>SCOPE (not what results page will look like)</a>
              </h1>
            </div>

            {/* <!-- Nav --> */}
            <nav id="nav">
              <ul>
                {/* <li><a href="left-sidebar.html">Left Sidebar</a></li> */}
                {/* <li><a href="right-sidebar.html">Right Sidebar</a></li> */}
                {/* <li><a href="no-sidebar.html">No Sidebar</a></li> */}
                <li>
                  <a href="/">Dashboard</a>
                </li>
                <li className="current">
                  <a href="/queries">Queries</a>
                </li>
                <li>
                  <a href="/results">Results</a>
                </li>
                {/* <li><a href='/login'>Login</a></li> */}
              </ul>
            </nav>
          </section>

          {/* <!-- Main --> */}
          <section id="main" className="wrapper style2">
            <div className="title">Queries</div>

            <input
              type="text"
              id="search"
              onkeyup="myFunction()"
              placeholder="Search queries.."
            />

            <table className="content-table" id="query-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Keywords</th>
                  <th>User</th>
                </tr>
              </thead>
              <tbody>
                {queries.map((query, i) => {
                  return (
                    <tr key={i}>
                      <td>{query.id}</td>
                      <td>{query.name}</td>
                      <td>{query.keywords.join(", ")}</td>
                      <td>{query.user}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <div className="container">
              {/* <!-- Features --> */}
              <section id="features">
                <ul className="actions special">
                  <li>
                    <a href="/create-query" className="button style1 large">
                      Create New Query
                    </a>
                  </li>
                </ul>
                {/* <button onClick={handleSubmit}>Look at Queries</button> */}
              </section>
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

export default Queries;
