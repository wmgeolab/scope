import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row } from "react-bootstrap";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import "bootstrap/dist/css/bootstrap.min.css";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Form from "react-bootstrap/Form";
import { Button } from "react-bootstrap";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import { GridToolbar } from "@mui/x-data-grid";
import Modal from "react-bootstrap/Modal";






const fake_data = [
  {
    id: 0,

    wsName: "article1",
    wsComments: "Argentina:Project",
    wsURL:
      "https://www.cbsnews.com/news/syria-airstrike-us-contractor-killed-iran-drone-attack-joe-biden-lloyd-austin/",
  },  
  {
    id: 1,

    wsName: "article2",
    wsURL:
      "https://www.washingtonpost.com/world/2023/03/24/rwanda-rusesabagina-release/",
  },
  {
    id: 2,
    wsName: "article3",
    wsURL:
      "https://www.politico.com/news/2023/03/24/democrats-tiktok-ban-china-00088659",
  },
  {
    id: 3,
    wsName: "article4",
    wsURL:
      "https://www.nytimes.com/2023/03/24/us/politics/house-approves-bill-requiring-schools-to-give-parents-more-information.html",
  },
];

const columns = [
  { field: "id", headerName: "ID", width: 90 },

  {
    field: "wsName",
    headerName: "Name",
    width: 150,
  },

  {
    field: "wsURL",
    headerName: "URL",
    width: 150,
    flex: 1,
    renderCell: (cellValue) => {
      //cell customization, make the name a link to the corresponding results page
      ///console.log(cellValue);mm
      return <a href={cellValue.formattedValue}>{cellValue.formattedValue}</a>;
    },
  },
];

const IndividualWorkspaces = () => {
  const { workspace_name } = useParams();
  console.log(workspace_name);

  // Used for the filtering model with the external search bar and the data grid.
  const [filt, setFilt] = useState([]);
  var textInput = React.createRef();
  const [show, setShow] = useState(false);

  const getAllArticles = async () => {

    // let response = await fetch(
    //   "http://127.0.0.1:8000/api/text/",
    //   {
    //     //results doesn't have anything in the array when printed
    //     headers: {
    //       "Content-Type": "application/json",
    //       Accept: "application/json",
    //       Authorization: "Token " + localStorage.getItem("user"),
    //     },
    //     body: JSON.stringify({
    //       "user" : localStorage.getItem("user"),
    //       "workspaceName": workspace_name
    //     })
    //   }
    // );
  
    // let q = await response.json();
  }

  const handleClose = () => {
    setShow(false);
  };

  const handleShow = () => {
    setShow(true);
  };

  const handleCopyClick = (params) => {
    navigator.clipboard.writeText(params);
  };

  // Handles logout with Github authentication.
  // Right now this is pretty janky as theres no set log out page or anything.
  const handleLogout = () => {
    localStorage.clear();
  };

  // Used to continuously keep track of what is in the search bar.
  // Ideally, it would need to only be passed once on a query being submitted.
  // TODO: Look into implementing that.
  const handleChange = () => {
    //can add this back later if needed, but commented out to make console happy since it was declared but never used
    // const value = textInput.current.value;
    //console.log(value);
  };

  // Used to handle keyword search with the search bar.
  // textInput is updated whenever there is a change and the string content can be accessed with textInput.current.value
  // onSubmitSearch is triggered when the user either triggers the search bar with the button (do we want this?) or hits enter.
  const onSubmitSearch = (event) => {
    event.preventDefault();
    console.log(
      "The input string being passed here is: ",
      textInput.current.value
    );

    // Right now - this is only filtering by name. Potentially: Add a dropdown menu allowing user to select which attribute they want to search it.
    setFilt([
      {
        columnField: "wsName",
        operatorValue: "contains",
        value: textInput.current.value,
      },
    ]);
  };

  if (localStorage.getItem("user") === null) {
    return (
      <div>
        <h1> 401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
        your access, please return to the <a href="/">dashboard</a> to log in
      </div>
    );
  } else {
    return (
      <div>
        {/* Scope Dashboard Header + Log Out Button */}
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
                <Container className="ms-auto">
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

        <div
          className="fullRowContainer"
          style={{ paddingTop: ".25%", paddingBottom: "2%", paddingLeft: "1%" }}
        >
          <Button
            variant="link"
            href="/workspaces"
            style={{
              fontFamily: "'Source Sans Pro', sans-serif",
              color: "rgb(48, 46, 46)",
              fontSize: "1.3ems",
            }}
          >
            🡸 Return home
          </Button>
        </div>

        {/* Container for the rest of the contents of the page
        Header, Dropdown Menus, Search Bar and Grid */}
        <Container>
          {/* Inline search bar and drop down menu. */}
          <Container>
            {/* Row for Go Back Button */}

            <Row>
              <div className="customRowContainer" s>
                {/* If we want to add a button here with the icon bar this is pretty easy. For now, the user can send input with the search bar. Just add 
                        <Button 
                        variant="light" 
                        type="text"
                        > */}

                {/* Column for Search Bar    */}

                <h2 className="wsHeadingsInternal">{workspace_name}</h2>

                <div className="workspaceSearchInternal">
                  <Form onSubmit={onSubmitSearch}>
                    <InputGroup>
                      <InputGroup.Text>
                        <Search></Search>
                      </InputGroup.Text>
                      <Form.Control
                        placeholder="Search by Article Name"
                        ref={textInput}
                        onChange={() => handleChange()}
                        type="text"
                      />
                    </InputGroup>
                  </Form>
                </div>
              </div>
            </Row>

            <Row>
              <div className="customRowContainer">
                <div className="individualTable">
                  <Box sx={{ height: 400, width: "100%" }}>
                    <DataGrid
                      rows={fake_data}
                      columns={columns}
                      pageSize={5}
                      rowsPerPageOptions={[5]}
                      checkboxSelection
                      disableColumnFilter
                      disableColumnMenu
                      disableDensitySelector
                      disableColumnSelector
                      disableSelectionOnClick
                      experimentalFeatures={{ newEditingApi: true }}
                      components={{ Toolbar: GridToolbar }}
                      filterModel={{
                        items: filt,
                      }}
                    />
                  </Box>
                </div>
              </div>
            </Row>
          </Container>

          {/* New row for add new workspace button. */}
          <Row className="text-center">
            <div className="add-new-button">
              <Button onClick={handleShow}>Share Workspace</Button>
            </div>
          </Row>

          <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
              <Modal.Title>Share Workspace Link</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <div>{"http://localhost:3000/workspace/" + workspace_name}</div>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-center">
              <Button
                variant="primary"
                onClick={() =>
                  handleCopyClick(
                    "http://localhost:3000/workspace/" + workspace_name
                  )
                }
              >
                Copy Link to Clipboard
              </Button>
            </Modal.Footer>
          </Modal>
        </Container>
      </div>
    );
  }
};

export default IndividualWorkspaces;
