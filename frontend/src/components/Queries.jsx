import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
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

const Queries = () => {
  const [queries, setQueries] = useState([]);
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowCount, setRowCount] = useState(0);
  const [checkboxSelection, setCheckboxSelection] = React.useState(true);

  const columns = [
    { field: "id", headerName: "ID", width: 150 },
    {
      field: "name",
      headerName: "Name",
      width: 150,
      renderCell: (cellValue) => {
        //cell customization, make the name a link to the corresponding results page
        return <a href={"/results/" + cellValue.id}>{cellValue.value}</a>;
      },
    },
    { field: "description", headerName: "Description", flex: 1, minWidth: 150 },
    { field: "user", headerName: "User", width: 150 },
    { field: "keywords", headerName: "Keywords", flex: 1, minWidth: 150 },
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

  //This is just temporary to make sure we keep updating the
  //run table while our source finding program is down
  // const addQueryRun = (query_id) => {

  //   var data = { queryId: query_id, };

  //   fetch("http://127.0.0.1:8000/api/run/", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: "Token " + localStorage.getItem("user"),
  //     },
  //     body: JSON.stringify(data)
  //   });
  //   console.log(JSON.stringify(data))

  // }

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

            <Box sx={{ height: 1000, width: "100%" }}>
              <DataGrid
                disableColumnFilter
                checkboxSelection={checkboxSelection}
                rows={queries}
                rowCount={rowCount}
                columns={columns}
                pageSize={15} //change this to change number of queries displayed per page, but should make backend
                pagination
                paginationMode="server"
                components={{
                  Pagination: CustomPagination,
                }}
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
