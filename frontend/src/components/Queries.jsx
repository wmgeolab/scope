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
import Pagination from "@mui/material/Pagination";
import PaginationItem from "@mui/material/PaginationItem";

import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/queries.css";

import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";

import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";

import Row from "react-bootstrap/Row";

const Queries = () => {
  const [queries, setQueries] = useState([]);
  const navigate = useNavigate();
  const [rowCount, setRowCount] = useState(0);
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();
  var [dropDownValue, setDropDownValue] = useState("Name");

  const handleChange = () => {
    const value = textInput.current.value;
  };

  const onSubmitSearch = (event) => {
    event.preventDefault();
    console.log(
      "The input string being passed here is: ",
      textInput.current.value
    );

    // Right now - this is only filtering by name. Potentially: Add a dropdown menu allowing user to select which attribute they want to search it.
    setFilt([
      {
        columnField: dropDownValue.toLowerCase(),
        operatorValue: "contains",
        value: textInput.current.value,
      },
    ]);
  };

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
      "http://127.0.0.1:8000/api/queries/?page=" + (curPage + 1), //have to add 1 becaues curPage is 0 indexed
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );
    console.log(response);
    console.log("user", localStorage.getItem("user"));
    let q = await response.json();

    console.log("q", q);

    setRowCount(q.count);
    setQueries(q.results);
    console.log("curpage", curPage);

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
                <Nav.Link href="/queries" className="nav-elements">
                  Queries
                </Nav.Link>
                <Nav.Link href="/workspaces" className="nav-elements">
                  Workspaces
                </Nav.Link>
                <Container class="ms-auto">
                  {/* <Button type="button" className="login">Hello</Button> */}

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

        <Row className="topper">
          <div className="headerWrapper">
            <h2 className="headings3">Queries</h2>
          </div>

          <div className="queryWrapper">
            <DropdownButton
              id="dropdown-basic-button"
              title={dropDownValue}
              style={{
                float: "right",
                marginRight: "0px",
                paddingTop: "40px",
                marginLeft: "50px",
              }}
              // className="querySelect"
            >
              <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
                Name
              </Dropdown.Item>
              <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
                Description
              </Dropdown.Item>
              <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
                Keywords
              </Dropdown.Item>
            </DropdownButton>
          </div>

          <div className="querySearch">
            {/* <img src={filter} width="40" height="40" alt="filter" display="inline" /> */}
            <Form onSubmit={onSubmitSearch}>
              <InputGroup>
                <InputGroup.Text>
                  <Search></Search>
                </InputGroup.Text>
                <Form.Control
                  placeholder="Search Queries"
                  ref={textInput}
                  onChange={() => handleChange()}
                  type="text"
                />
              </InputGroup>
            </Form>
          </div>
        </Row>

        <Box className="table" sx={{ height: 400, width: "100%" }}>
          <DataGrid
            disableColumnFilter
            rows={queries}
            rowCount={rowCount}
            columns={columns}
            pageSize={15} //change this to change number of queries displayed per page, but should make backend
            pagination
            paginationMode="server"
            checkboxSelection
            components={{
              Pagination: CustomPagination,
            }}
            onPageChange={(newPage) => handleSubmit(newPage)}
            filterModel={{
              items: filt,
            }}
          />
        </Box>

        <div>
          {/* <!-- Features --> */}
          <section id="features" className="centerButtonAlign">
            {/* <ul className="actions special">
                  <li>
                    <a href="/create-query" className="button style1 large">
                      Create New Query
                    </a>
                  </li>
                </ul> */}
            <Button href="/create-query" className="centerButton">
              Create New Query
            </Button>
          </section>
        </div>
        {/* </section> */}
        {/* </div> */}

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
