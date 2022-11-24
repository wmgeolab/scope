import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";

const Queries = () => {
  const [queries, setQueries] = useState([]);
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowCount, setRowCount] = useState(0);

  const columns = [
    { field: "id", headerName: "ID", width: 150 },
    { field: "name", headerName: "Name", width: 150 },
    { field: "description", headerName: "Description", width: 150 },
    { field: "user", headerName: "User", width: 150 },
    { field: "keywords", headerName: "Keywords", width: 150 },
  ];

  const handleSubmit = async (curPage) => {
    console.log("handlesubmit:", curPage);
    let response = await fetch(
      "http://127.0.0.1:8000/api/queries/?page=" + (curPage + 1),
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );
    console.log(response);
    console.log(localStorage.getItem("user"));
    let q = await response.json();

    console.log(q);

    setRowCount(q.count);
    setQueries(q.results);
    setPage(curPage);
    return q;
  };

  useEffect(() => {
    handleSubmit(0);
  }, []); //listening on an empty array

  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
    navigate("/");
  };

  function search() {
    {
      /* need to fix the search so it goes through all data rather than just current page*/
    }
    // Declare variables
    var input, filter, table, tr, td1, td2, i, txtValue1, txtValue2;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("query-table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td1 = tr[i].getElementsByTagName("td")[1];
      td2 = tr[i].getElementsByTagName("td")[2];
      if (td1 && td2) {
        txtValue1 = td1.textContent || td1.innerText;
        txtValue2 = td2.textContent || td2.innerText;
        if (
          txtValue1.toUpperCase().indexOf(filter) > -1 ||
          txtValue2.toUpperCase().indexOf(filter) > -1
        ) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
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
                <li>
                  <a href="/">Dashboard</a>
                </li>
                <li className="current">
                  <a href="/queries">Queries</a>
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
              onKeyUp={search}
              placeholder="Search queries.."
            />
            <Box sx={{ height: 400, width: "100%" }}>
              <DataGrid
                rows={queries}
                rowCount={rowCount}
                columns={columns}
                pageSize={5} //change this to change number of queries displayed per page, but should make backend
                pagination
                paginationMode="server"
                onPageChange={(newPage) => handleSubmit(newPage)}
              />
            </Box>
            {/* {console.log(queries)} */}
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
