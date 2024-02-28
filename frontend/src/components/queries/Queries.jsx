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
import "../../assets/css/queries.css"
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Row from "react-bootstrap/Row";
import UnauthorizedView from "../UnauthorizedView";

const Queries = (props) => {
  const {
    loggedIn
  } = props;

  const [queries, setQueries] = useState([]);
  const navigate = useNavigate();
  const [rowCount, setRowCount] = useState(0);
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();
  var [dropDownValue, setDropDownValue] = useState("Name");

  const handleChange = () => {
    // const value = textInput.current.value;
  };

  const onSubmitSearch = (event) => {
    event.preventDefault();
    console.log(
      "The input string being passed here is: ",
      textInput.current.value
    );

    setFilt([
      {
        columnField: dropDownValue.toLowerCase(),
        operatorValue: "contains",
        value: textInput.current.value,
      },
    ]);
  };

  //the content of the columns for the datagrid that contains the queries
  const columns = [
    { field: "id", headerName: "ID", width: 150 },
    {
      field: "name",
      headerName: "Name",
      width: 150,
      renderCell: (cellValue) => {
        //cell customization, makes the name a link to the corresponding results page
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

    console.log("Response:", q);

    setRowCount(q.count);
    setQueries(q.results);

    return q;
  };

  useEffect(() => {
    handleSubmit(0);
  }, []); //listening on an empty array

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

  if (loggedIn === false) {
    // fix?
    return <UnauthorizedView />;
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
        {/* Container for the rest of the contents of the page
        Header, Dropdown Menus, Search Bar and Grid */}
        <Container>
          <div
            className="customRowContainer"
            style={{ paddingBottom: "2%", paddingTop: "1%" }}
          >
            <h2 style={{ paddingTop: "1%", fontWeight: "bold " }}>Queries</h2>
          </div>
          {/* Inline search bar and drop down menu. */}
          <Row>
            <div className="customRowContainer">
              <DropdownButton
                id="dropdown-basic-button"
                title={dropDownValue}
                style={{ float: "right", marginLeft: "10px" }}
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
            </div>
          </Row>

          {/* QUERIES TABLE */}
          <Row>
            <div className="customRowContainer">
              <div className="individualTable">
                <Box sx={{ height: 400, width: "100%" }}>
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
              </div>
            </div>
          </Row>

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
        </Container>

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
