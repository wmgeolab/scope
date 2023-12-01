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
import Pagination from "@mui/material/Pagination";
import PaginationItem from "@mui/material/PaginationItem";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/results.css";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import ScopeNavBar from "./ScopeNavBar";
import UnauthorizedView from "./UnauthorizedView";

const Results = (props) => {
  const {
    loggedIn
  } = props;
  //gets the queryName from the URL
  const { query_id } = useParams();
  const [rowCount, setRowCount] = useState(0);
  const [queryResults, setQueryResults] = useState([]);
  const navigate = useNavigate();
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();
  const [queryName, setQueryName] = useState("");
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [selectedWorkspace, setSelectedWorkspace] = useState(1);
  const [location, setLocation] = useState("US");
  const [language, setLanguage] = useState("English");

  const [dropClicked, setDropClicked] = useState(false);

  var listCheck = React.createRef();

  //   listCheck.onClick = function(evt) {
  //   if (listCheck.classList.contains('visible'))
  //     listCheck.classList.remove('visible');
  //   else
  //     listCheck.classList.add('visible');
  // }

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

        // Cell value id -> article id #
        // Cell Value Value -> Article title to be displayed.

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

  //add back in when error is fixed

  // const handleTitle = async (curPage) => {
  //   console.log("handlesubmit:", curPage);
  //   let response = await fetch(
  //     "http://127.0.0.1:8000/api/queries/?page=" + (curPage + 1), //have to add 1 becaues curPage is 0 indexed
  //     {
  //       headers: {
  //         "Content-Type": "application/json",
  //         Authorization: "Token " + localStorage.getItem("user"),
  //       },
  //     }
  //   );
  //   console.log(response);
  //   console.log("user", localStorage.getItem("user"));
  //   let q = await response.json();

  //   var result = Array.isArray(q.results)
  //     ? q.results.find((item) => item.id === Number(query_id))
  //     : -1;
  //   setQueryName(result.name);

  //   // console.log("curpage", curPage);
  // };

  useEffect(() => {
    handleSubmit(0);
    //add back in when error is fixed

    //handleTitle(0);
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
        <link rel="stylesheet" href="assets/css/table.css" />
        <link rel="stylesheet" href="assets/css/main.css" />
        <div id="page-wrapper">
          {/* <!-- Main --> */}
          <section id="main" className="wrapper style2">
            <h2 className="headings3">Results for {queryName}</h2>

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

            {/* add back in later with relevant search options when we have them */}
            <div
              id="list1"
              className="dropdown-check-list"
              ref={listCheck}
              tabindex="100"
            >
              <span
                className="anchor"
                onClick={() => {
                  dropClicked ? setDropClicked(false) : setDropClicked(true);
                }}
                style={dropClicked ? { color: "#0094ff" } : {}}
              >
                Select Location
              </span>
              <ul
                className="items"
                style={dropClicked ? { display: "block" } : {}}
              >
                <li>
                  <input type="checkbox" />
                  US{" "}
                </li>
                <li>
                  <input type="checkbox" />
                  China
                </li>
                <li>
                  <input type="checkbox" />
                  Russia{" "}
                </li>
                <li>
                  <input type="checkbox" />
                  Ukraine{" "}
                </li>
                <li>
                  <input type="checkbox" />
                  Argentina{" "}
                </li>
                <li>
                  <input type="checkbox" />
                  Sudan{" "}
                </li>
                <li>
                  <input type="checkbox" />
                  Iran
                </li>
              </ul>
            </div>

            {/* placeholders for later options */}

            {/* <DropdownButton id="dropdown-basic-button" title="Language">
                <Dropdown.Item onClick={(e) => setLanguage(e.target.text)}>
                  English
                </Dropdown.Item>
                <Dropdown.Item onClick={(e) => setLanguage(e.target.text)}>
                  Chinese
                </Dropdown.Item>
                <Dropdown.Item onClick={(e) => setLanguage(e.target.text)}>
                  Russian
                </Dropdown.Item>
              </DropdownButton> */}
            {/* <DropdownButton
          id="dropdown-basic-button"
          title="Date Range"
        >
          <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
            China
          </Dropdown.Item>
          <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
            US
          </Dropdown.Item>
          <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
            Russia
          </Dropdown.Item>
        </DropdownButton> */}
            {/* </div> */}

            {/*We want:
        - button is just a static title,
        - dropdown has checklist to select multiple */}

            {/* <Form.Control
          as="select"
          aria-label="Options"
          name="type"
          size="sm"
          onChange={(e) => {
            console.log("e.target.value", e.target.value);
            // handleOptionChange(e, index);
          }}
          // value={}
        >
          <option value="operation">Operation</option>
          <option value="inputoutput">Input/Output</option>
          <option value="subroutine">Subroutine</option>
          <option value="condition">Condition</option>
          <option value="parallel">Parallel</option>
        </Form.Control> */}

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
                onSelectionModelChange={(ids) => {
                  const selectedIDs = new Set(ids);
                  const selectedRows = queryResults.filter((row) =>
                    selectedIDs.has(row.id)
                  );

                  console.log("check", selectedRows);
                }}
                filterModel={{
                  items: filt,
                }}
              />
            </Box>

            <div>
              <section id="features" className="centerButtonAlign">
                <Button className="centerButton" onClick={handleShow}>
                  Send Selected to Workspace
                </Button>
              </section>
            </div>

            <Modal show={show} onHide={handleClose}>
              <Modal.Header closeButton>
                <Modal.Title>Send to Workspace</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <p>Choose a Workspace:</p>
                <Form.Select
                  aria-label="Default select example"
                  value={selectedWorkspace}
                  onChange={(e) => {
                    console.log(e.target.value);
                    setSelectedWorkspace(e.target.value);
                  }}
                >
                  <option value="1">One</option>
                  <option value="2">Two</option>
                  <option value="3">Three</option>
                </Form.Select>
              </Modal.Body>
              <Modal.Footer>
                <Button onClick={handleClose}>
                  Send Selected to Workspace
                </Button>
                <Button variant="secondary" onClick={handleClose}>
                  Cancel
                </Button>
              </Modal.Footer>
            </Modal>
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
