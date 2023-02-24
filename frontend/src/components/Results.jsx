import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Route, useNavigate, useParams } from "react-router-dom";
import Dashboard from "./Dashboard";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";
import Box from "@mui/material/Box";
import {
  DataGrid,
  gridPageCountSelector,
  gridPageSelector,
  useGridApiContext,
  useGridSelector,
} from "@mui/x-data-grid";
// import { useDemoData } from "@mui/x-data-grid-generator";
// import { styled } from "@mui/material/styles";
import Pagination from "@mui/material/Pagination";
import PaginationItem from "@mui/material/PaginationItem";

const Results = () => {
  //gets the queryName from the URL
  const { query_id } = useParams();
  const [page, setPage] = useState(0);
  const [rowCount, setRowCount] = useState(0);
  const [queryResults, setQueryResults] = useState([]);
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();

  // for the checkbox, add functionality later
  // const label = { inputProps: { "aria-label": "Checkbox demo" } };
  const columns = [
    { field: "id", headerName: "ID", width: 150 },
    {
      field: "text",
      headerName: "Text",
      flex: 1,
      minWidth: 150,
    },
    {
      field: "url",
      headerName: "URL",
      flex: 1,
      minWidth: 150,
      renderCell: (cellValue) => {
        //cell customization, make the name a link to the corresponding results page
        return <a href={cellValue.value}>{cellValue.value}</a>;
      },
    },
  ];

  const handleSubmit = async (curPage) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/sources/" +
        query_id +
        "/?page=" +
        (curPage + 1),
      {
        ///results doesn't have anything in the array when printed
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );
    let q = await response.json();

    console.log(q);
    console.log(q[0]);
    const new_q = [];
    for (let i = 0; i < q.length; i++) {
      var dict = {
        id: q[i].pk,
        text: q[i]["fields"]["text"],
        url: q[i]["fields"]["url"],
      };
      new_q[i] = dict;
    }
    setRowCount(new_q.length);
    setPage(curPage);
    console.log(new_q);
    console.log(new_q.length);
    setQueryResults(new_q);
    return new_q;
  };

  useEffect(() => {
    handleSubmit(0);
  }, []); //listening on an empty array

  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
    navigate("/");
  };

  function CustomPagination() {
    const apiRef = useGridApiContext();
    const page = useGridSelector(apiRef, gridPageSelector);
    const pageCount = useGridSelector(apiRef, gridPageCountSelector);

    return (
      <Pagination
        color="primary"
        variant="outlined"
        shape="rounded"
        page={page + 1}
        count={pageCount}
        // @ts-expect-error
        renderItem={(props2) => <PaginationItem {...props2} disableRipple />}
        onChange={(event, value) => apiRef.current.setPage(value - 1)}
      />
    );
  }

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
            <button onClick={handleLogout}>Logout</button>{" "}
            {/*try putting the button in a mui box to move it*/}
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

            <Box sx={{ height: 400, width: "100%" }}>
              <DataGrid
                disableColumnFilter
                rows={queryResults}
                rowCount={rowCount}
                columns={columns}
                pageSize={5} //change this to change number of queries displayed per page, but should make backend
                checkboxSelection
                pagination
                paginationMode="server"
                components={{
                  Pagination: CustomPagination,
                }}
                onPageChange={(newPage) => handleSubmit(newPage)}
              />
            </Box>
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
