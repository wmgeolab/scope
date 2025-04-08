import React, { useState, useEffect, useRef } from "react";
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
import Modal from "react-bootstrap/Modal";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Row from "react-bootstrap/Row";
import UnauthorizedView from "../UnauthorizedView";
import { TailSpin } from "react-loader-spinner";
import { API } from "../../api/api";




const Queries = (props) => {
  const { loggedIn } = props;

  //const [queries, setQueries] = useState([]);
  const [sources, setSources] = useState([])
  const [rowCount, setRowCount] = useState(0);
  const [filt, setFilt] = useState([]);
  //var textInput = React.createRef();
  const textInput = useRef(null);
  var [dropDownValue, setDropDownValue] = useState("Text");
  const [loading, setLoading] = useState(true);

  // State for row selection (for sending to workspace)
  const [selectedRows, setSelectedRows] = useState([]);

  // States for workspace modal and data:
  const [show, setShow] = useState(false);
  const [workspaceData, setWorkspaceData] = useState([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState("");
  

  // const fetchQueries = async (curPage) => {
  //   setLoading(true); // Set loading to true when fetching data
  //   try {
  //     const response = await fetch(
  //       API.url(`/api/queries/?page=${curPage + 1}`), //have to add 1 becaues curPage is 0 indexed
  //       {
  //         headers: API.getAuthHeaders(),
  //       }
  //     );
  //     const data = await response.json();
  //     setRowCount(data.count);
  //     setQueries(data.results);
  //   } catch (error) {
  //     console.error("Error fetching queries:", error);
  //   } finally {
  //     setLoading(false); // Set loading to false after data fetching is complete
  //   }
  // };

  const fetchSources = async (curPage, searchTerm="") => {
    setLoading(true);
    try {
      const url =
        API.url(`/api/sources/?page=${curPage + 1}`) +
        (searchTerm ? `&search=${encodeURIComponent(searchTerm)}` : "");
      const response = await fetch(url, {
        headers: API.getAuthHeaders(),
      });
      const data = await response.json();
      setRowCount(data.count);
      setSources(data.results);
    } catch (error) {
      console.error("Error fetching sources:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    //fetchQueries(0); // Fetch queries on component mount
    fetchSources(0);
  }, []);


  const onSubmitSearch = (event) => {
    event.preventDefault();
    const searchValue = textInput.current.value;
    

    setFilt([
      {
        columnField: dropDownValue.toLowerCase(),
        operatorValue: "contains",
        value: searchValue,
      },
    ]);
    fetchSources(0, searchValue);
  };

  //the content of the columns for the datagrid that contains the queries
  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "url",
      headerName: "URL",
      width: 300,
      renderCell: (cellValue) => {
        return (
          <a href={"/display-article/" + cellValue.id} target="_blank" rel="noopener noreferrer">
            {cellValue.value}
          </a>
        );
      },
    },
    { field: "text", headerName: "Text", flex: 1, minWidth: 150 },
    // { field: "user", headerName: "User", width: 150 },
    // { field: "keywords", headerName: "Keywords", flex: 1, minWidth: 150 },
  ];

  // const handleSubmit = async (curPage) => {
  //   console.log("handlesubmit:", curPage);
  //   let response = await fetch(
  //     API.url(`/api/queries/?page=${curPage + 1}`), // have to add 1 becaues curPage is 0 indexed
  //     {
  //       headers: API.getAuthHeaders(),
  //     }
  //   );

  //   console.log(response);
  //   console.log("user", localStorage.getItem("user"));
  //   let q = await response.json();

  //   console.log("Response:", q);

  //   setRowCount(q.count);
  //   setQueries(q.results);

  //   return q;
  // };

  // useEffect(() => {
  //   handleSubmit(0);
  // }, []); //listening on an empty array

  // Handle server-side paging when the page is changed.
  const handlePageChange = (curPage) => {
    const searchValue = textInput.current ? textInput.current.value : "";
    fetchSources(curPage, searchValue);
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

  // --- Workspace Modal and Send Functionality ---

  // Handlers for showing/closing the modal.
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // Fetch workspace data that the current user is part of.
  const gatherWorkspaces = async () => {
    try {
      const response = await fetch(API.url("/api/workspaces/"), {
        headers: API.getAuthHeaders(),
      });
      const responseData = await response.json();
      // Transform the response to get a list of { id, name }:
      const formatted = responseData.results.map((result) => ({
        id: result.workspace.id,
        name: result.workspace.name,
      }));
      setWorkspaceData(formatted);
      if (formatted && formatted.length > 0) {
        setSelectedWorkspace(formatted[0].id);
      }
    } catch (error) {
      console.error("Error fetching workspaces:", error);
    }
  };

  useEffect(() => {
    gatherWorkspaces();
  }, []);

  // Send selected sources to the chosen workspace.
  const putSources = async () => {
    console.log("Selected workspace: ", selectedWorkspace);
    console.log("Selected Sources: ", selectedRows)
    if (!selectedWorkspace) return;
    for (let source of selectedRows) {
      const data = {
        workspace: selectedWorkspace,
        source_id: source.id,
      };
      try {
        const response = await fetch(API.url("/api/entries/"), {
          method: "POST",
          headers: {
            ...API.getAuthHeaders(),
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        const resData = await response.json();
        console.log("Response:", resData);
      } catch (error) {
        console.error("Error sending source to workspace:", error);
      }
    }
  };

  // Handle the "send" button click inside the modal.
  const handleSend = () => {
    putSources();
    setShow(false);
  };

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
                  Text
                </Dropdown.Item>
                {/* <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
                  Description
                </Dropdown.Item>
                <Dropdown.Item onClick={(e) => setDropDownValue(e.target.text)}>
                  Keywords
                </Dropdown.Item> */}
              </DropdownButton>

              <div className="querySearch">
                
                {/* <img src={filter} width="40" height="40" alt="filter" display="inline" /> */}
                <Form onSubmit={onSubmitSearch}>
                  <InputGroup>
                    <InputGroup.Text>
                      <Search></Search>
                    </InputGroup.Text>
                    <Form.Control
                      placeholder="Search Sources"
                      ref={textInput}
                      //onChange={() => handleChange()}
                      type="text"
                    />
                  </InputGroup>
                </Form>
              </div>
            </div>
          </Row>

          {/* SOURCES TABLE */}
          
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
                        rows={sources}
                        rowCount={rowCount}
                        columns={columns}
                        pageSize={15}
                        pagination
                        paginationMode="server"
                        checkboxSelection
                        // Controlled selection: make sure selectedRows is an array of IDs.
                        selectionModel={selectedRows.map((row) => row.id)}
                        components={{
                          Pagination: CustomPagination,
                        }}
                        onPageChange={(newPage) => handlePageChange(newPage)}
                        onSelectionModelChange={(newSelection) => {
                          console.log("onSelectionModelChange triggered", newSelection);
                          // Convert selected values to strings and compare with row.id as string.
                          const selectedIDs = new Set(newSelection.map(String));
                          const selectedData = sources.filter((row) =>
                            selectedIDs.has(String(row.id))
                          );
                          console.log("Selected Rows: ", selectedData);
                          setSelectedRows(selectedData);
                        }}
                        filterModel={{ items: filt }}
                      />
                    )}
                  </Box>
                </div>
              </div>
            


          <div>
            {/* <!-- Features --> */}
            <section id="features" className="centerButtonAlign">
              <Button className="centerButton" onClick={handleShow}>
                Send Selected to Workspace
              </Button>
            </section>
          </div>

          {/* Modal for choosing workspace and sending selected sources */}
          <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
              <Modal.Title>Send to Workspace</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {workspaceData === undefined || workspaceData.length === 0 ? (
                <p>Please join or create a workspace first!</p>
              ) : (
                <Form.Group controlId="workspaceSelect">
                  <Form.Label>Choose a Workspace:</Form.Label>
                  <Form.Control
                    as="select"
                    value={selectedWorkspace}
                    onChange={(e) => setSelectedWorkspace(e.target.value)}
                  >
                    {workspaceData.map((workspace) => (
                      <option key={workspace.id} value={workspace.id}>
                        {workspace.name}
                      </option>
                    ))}
                  </Form.Control>
                </Form.Group>
              )}
            </Modal.Body>
            <Modal.Footer>
              <Button
                onClick={handleSend}
                disabled={!workspaceData || workspaceData.length === 0}
              >
                Send Selected to Workspace
              </Button>
              <Button variant="secondary" onClick={handleClose}>
                Cancel
              </Button>
            </Modal.Footer>
          </Modal>
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
