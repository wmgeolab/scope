import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
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

import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";

import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/results.css";

import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import filter from "./../images/icons/filtering_queries.png";


const Results = () => {
  //gets the queryName from the URL
  const { query_id } = useParams();
  const [rowCount, setRowCount] = useState(0);
  const [queryResults, setQueryResults] = useState([]);
  const navigate = useNavigate();
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();

  const handleChange = () => {
    const value = textInput.current.value;
  };

  const onSubmitSearch = (event) => {
    event.preventDefault();
    console.log(
      "The input string being passed here is: ",
      textInput.current.value
    );

    setFilt([
      {
        columnField: "text",
        operatorValue: "contains",
        value: textInput.current.value,
      },
    ]);
  };

  // for the checkbox, add functionality later
  // const label = { inputProps: { "aria-label": "Checkbox demo" } };
  const columns = [
    { field: "id", headerName: "ID", width: 150 },
    {
      field: "text",
      headerName: "Text",
      flex: 1,
      minWidth: 150,
      renderCell: (cellValue) => {
        //cell customization, make the name a link to the corresponding article that will be displayed
        return (
          <a href={"/display-article/" + cellValue.id}>{cellValue.value}</a>
        );
      },
    },
    {
      field: "url",
      headerName: "Article",
      flex: 1,
      minWidth: 150,
      renderCell: (cellValue) => {
        //cell customization, add the url to the source/result
        return <a href={cellValue.value}>{cellValue.value}</a>;
      },
    },
  ];

  const handleSubmit = async (curPage) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/sources/" +
        query_id +
        "/" +
        (curPage + 1) +
        "/?page=" +
        (curPage + 1),
      {
        //results doesn't have anything in the array when printed
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );
    let q = await response.json();

    console.log("q", q);
    console.log("first", q[0]);
    const new_q = [];
    for (let i = 0; i < q.length; i++) {
      var dict = {
        id: q[i].pk,
        text: q[i]["fields"]["text"],
        url: q[i]["fields"]["url"],
      };
      new_q[i] = dict;
    }
    //setRowCount(new_q.length);
    console.log("new_q", new_q);
    console.log("length", new_q.length);
    console.log("page:", curPage);
    setQueryResults(new_q);

    //this is the fetch request to get the source count
    let countResponse = await fetch(
      "http://127.0.0.1:8000/api/count/" + query_id + "/",
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );

    let x = await countResponse.json();
    console.log("Source count: ", x);

    setRowCount(x);

    return new_q;
  };

  useEffect(() => {
    handleSubmit(0);
  }, []); //listening on an empty array

  const handleLogout = () => {
    localStorage.clear();
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
          <Navbar bg="dark" variant="dark" className="nav">
            <Container>
              <Navbar.Brand className="nav-title">
                <img
                  src={logo}
                  width="30"
                  height="30"
                  className="d-inline-block align-top"
                  alt="Scope logo"
                />{" "}
                SCOPE
              </Navbar.Brand>

              <Navbar.Toggle aria-controls="basic-navbar-nav" />

              <Navbar.Collapse>
                <Nav className="flex-grow-1 justify-content-evenly">
                  <Nav.Link href="/" className="nav-elements">
                    Home
                  </Nav.Link>
                  {/* /queries or else will go to /results/queries instead */}
                  <Nav.Link href="/queries" className="nav-elements">
                    Queries
                  </Nav.Link>
                  <Nav.Link href="/workspaces" className="nav-elements">
                    Workspaces
                  </Nav.Link>
                  <Container class="ms-auto">
                    <div style={{ paddingLeft: 100 }}>
                      <Button
                        type="button"
                        className="login"
                        onClick={handleLogout}
                        style={{ justifyContent: "right" }}
                      >
                        Log Out
                      </Button>
                    </div>
                  </Container>
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>

          {/* <!-- Main --> */}
          <section id="main" className="wrapper style2">
            <h2 className="headings3">Results for []</h2>

            <div className="resultSearch">
              {/* <img src={filter} width="40" height="40" alt="filter" display="inline" /> */}
              <Form onSubmit={onSubmitSearch}>
                <InputGroup>
                  <InputGroup.Text>
                    <Search></Search>
                  </InputGroup.Text>
                  <Form.Control
                    placeholder="Search Results"
                    ref={textInput}
                    onChange={() => handleChange()}
                    type="text"
                  />
                </InputGroup>
              </Form>
            </div>

            <Box className="table" sx={{ height: 400, width: "100%" }}>
              <DataGrid
                disableColumnFilter
                // checkboxSelection={checkboxSelection}
                checkboxSelection
                rows={queryResults}
                rowCount={rowCount}
                columns={columns}
                pageSize={5} //change this to change number of queries displayed per page, but should make backend
                pagination
                paginationMode="server"
                components={{
                  Pagination: CustomPagination,
                  toolbar: {
                    showQuickFilter: true,
                    quickFilterProps: { debounceMs: 500 },
                  },
                }}
                onPageChange={(newPage) => handleSubmit(newPage)}
                filterModel={{
                  items: filt,
                }}
              />
            </Box>

            <div>
              <section id="features" className="centerButtonAlign">
                <Button href="/" className="centerButton">
                  Send Selected to Workspace
                </Button>
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
