import React, { useState, useEffect } from "react";
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
import "../../assets/css/queries.css";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Row from "react-bootstrap/Row";
import UnauthorizedView from "../UnauthorizedView";
import { TailSpin } from "react-loader-spinner";
import { API } from "../../api/api";




const Queries = (props) => {
  const { loggedIn } = props;

  const [queries, setQueries] = useState([]);
  const [rowCount, setRowCount] = useState(0);
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();
  var [dropDownValue, setDropDownValue] = useState("Name");
  const [loading, setLoading] = useState(true);
  


  const handleChange = () => {
    // const value = textInput.current.value;
  };


  const fetchQueries = async (curPage) => {
    setLoading(true); // Set loading to true when fetching data
    try {
      const response = await fetch(
        API.url(`/api/queries/?page=${curPage + 1}`), //have to add 1 becaues curPage is 0 indexed
        {
          headers: API.getAuthHeaders(),
        }
      );
      const data = await response.json();
      setRowCount(data.count);
      setQueries(data.results);
    } catch (error) {
      console.error("Error fetching queries:", error);
    } finally {
      setLoading(false); // Set loading to false after data fetching is complete
    }
  };

  useEffect(() => {
    fetchQueries(0); // Fetch queries on component mount
  }, []);


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
      API.url(`/api/queries/?page=${curPage + 1}`), // have to add 1 becaues curPage is 0 indexed
      {
        headers: API.getAuthHeaders(),
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
            // style={{ paddingBottom: "2%", paddingTop: "1%" }}
          >
            <h2 style={{ paddingTop: "2%", paddingBottom: "2%", fontWeight: "bold " }}>Sources</h2>
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
          
              <div className="customRowContainer">
                <div className="individualTable">
                  <Box sx={{ height: 400, width: "100%" }}>
                    {/* Conditionally render loading spinner */}
                    {loading ? (
                      <div className="loader-container d-flex justify-content-md-center"> {/* Center the loader vertically and horizontally */}
                        <TailSpin
                          color="#00BFFF"
                          height={100}
                          width={100}
                        />
                        
                      </div>
                    ) : (
                      // Render data grid when loading is complete
                      <DataGrid
                        disableColumnFilter
                        rows={queries}
                        rowCount={rowCount}
                        columns={columns}
                        pageSize={15}
                        pagination
                        paginationMode="server"
                        checkboxSelection
                        components={{
                          Pagination: CustomPagination,
                        }}
                        onPageChange={(newPage) => fetchQueries(newPage)}
                        filterModel={{
                          items: filt,
                        }}
                      />
                    )}
                  </Box>
                </div>
              </div>
            


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
                Send to Workspace
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
