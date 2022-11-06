import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Route, useNavigate, useParams } from "react-router-dom";
import Dashboard from "./Dashboard";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";

const Results =  () => {
  //gets the queryName from the URL
  const {queryName} = useParams();

  const [queryResults, setQueryResults] = useState([]);
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();
  // for the checkbox, add functionality later
  const label = { inputProps: { "aria-label": "Checkbox demo" } };

  // Data from `Route` will be passed as a prop.
// function UserPage({ props }) {
//   return (
//     <div>
//       {/* The URL is passed as `match.url`. */}
//       {/* `props.url` and `props.path` will be defined whether or not the path is parameterized. */}
//       <div>{`The URL is "${props.url}"!`}</div>
//       {/* The path (the one you gave `Route`) is passed as `props.path`. */}
//       <div>{`It matched the path "${props.path}"!`}</div>
//       {/* The parameters are passed as `props.params`. */}
//       <div>{`The parameter is "${props.params.username}"!`}</div>
//     </div>
//   );
// }

  const handleSubmit = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/sources/", {
      ///results doesn't have anything in the array when printed
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    let q = await response.json();

    console.log(q);
    setQueryResults(q.results);

    return q;
  };

  useEffect(() => {
    handleSubmit();
  }, []); //listening on an empty array

  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
    navigate("/");
  };

  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      <div>
        Oops, looks like you've exceeded the SCOPE of your access, please return
        to the <a href="/">dashboard</a> to log in
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
    // alert("Please log in")
  } else {
    return (
      <div>
        {/* <button onClick={handleLogout}>Logout</button> */}
        <div>{`The parameter is "${queryName}"!`}</div>
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
          <button onClick={handleLogout}>Logout</button>  {/*try putting the button in a mui box to move it*/}
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
                <li>
                  <a href="/">Dashboard</a>
                </li>
                <li className="current">
                  <a href="/queries">Queries</a>
                </li>
                {/* <li>
                  <a href="/results">Results</a>
                </li> */}
                {/* <li><a href='/login'>Login</a></li> */}
              </ul>
            </nav>
          </section>

          {/* <!-- Main --> */}
          <section id="main" className="wrapper style2">
            <div className="title">Results</div>

            <input
              type="text"
              id="search"
              onkeyup="myFunction()"
              placeholder="Search results.."
            />

            <table className="content-table" id="query-table">
              <thead>
                <tr>
                  <the></the>
                  <th>ID</th>
                  <th>Text</th>
                  <th>url</th>
                </tr>
              </thead>
              <tbody>
                {queryResults.map((result, i) => { 
                  return (
                    <tr key={i}>
                      <Checkbox {...label} color="secondary" />

                      <td>{result.id}</td>
                      <td>{result.text}</td>
                      <a href={result.url}>
                        <td>{result.url}</td>
                      </a>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <div className="container">
              {/* <!-- Features --> */}
              <section id="features">
                <ul className="actions special"></ul>
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

export default Results;
