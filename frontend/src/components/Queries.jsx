import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
const Queries = () => {
  const [queries, setQueries] = useState([]);

  const handleSubmit = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/queries/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    let q = await response.json();

    console.log(q);
    setQueries(q);
    return q;
    //   .then((res) => res.json())
    //   .then((response) => {
    //     console.log("Success: ", JSON.stringify(response));
    //   })
    //   .catch((error) => console.error("Error: ", error));
  };

  useEffect(() => {
    handleSubmit();
  }, []); //listening on an empty array

  if(localStorage.getItem("user") === null) {    // fix?
    return(
      <div>
      <h2>lol</h2>
    </div>
    );
  }
  else {
    return (
      <div>
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
            <table className="content-table">
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
  
            {/* <table className="content-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Keywords</th>
                  <th>User</th>
                </tr>
              </thead>
              <tbody>
                 <tr>
                  <td>1</td>
                  <td>
                    <a href="/">Russian hydroelectric activity in Africa</a>
                  </td>
                  <td>Russia, Water, Africa</td>
                  <td>michaelrfoster</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>
                    <a href="/">Covid-19 impact on USA vs Russia</a>
                  </td>
                  <td>Covid, USA, Russia</td>
                  <td>LazyRiver18</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>
                    <a href="/">
                      Food shortages in Ukrane resulting from Russian invasion
                    </a>
                  </td>
                  <td>Ukrane, Russia, Food, Shortages</td>
                  <td>istwu</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>
                    <a href="/">Recent communication between China and Russia</a>
                  </td>
                  <td>China, Russia, Talks</td>
                  <td>devsaxena974</td>
                </tr>
              </tbody>
            </table> */}
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
