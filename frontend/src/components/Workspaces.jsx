import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row } from "react-bootstrap";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/workspace.css";
import { DataGrid } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Form from "react-bootstrap/Form";
import { Button } from "react-bootstrap";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import { GridToolbar } from "@mui/x-data-grid";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

import Modal from "react-bootstrap/Modal";

const fake_data = [
  {
    id: 0,
    wsOwner: "user1",
    wsName: "My Workspace 1",
    wsTags: "Argentina",
  },
  {
    id: 1,
    wsOwner: "user2",
    wsName: "My Workspace 2",
  },
  {
    id: 2,
    wsOwner: "user3",
    wsName: "My Workspace 3",
    wsTags: "please,help",
  },
  {
    id: 3,
    wsOwner: "user4",
    wsName: "My Workspace 4",
    wsTags: "Ukraine",
  },
];

const Workspaces = () => {
  // Used for the filtering model with the external search bar and the data grid.
  const [filt, setFilt] = useState([]);
  const navigate = useNavigate();
  var textInput = React.createRef();
  var [dropDownValue, setValue] = useState("All Workspaces");
  var [dropDownValueSearch, setDropDownValueSearch] = useState("Owner");
  var [wsMakeName, setMakeName] = useState("");
  var [wsMakePassword, setMakePassword] = useState("");
  var [wsJoinName, setJoinName] = useState("");
  var [wsJoinPassword, setJoinPassword] = useState("");
  const [formValid, setFormValid] = useState(false);
  const [errorState, setErrorState] = useState(false);

  // const getAllWorkspaces = async () => {

  //   let response = await fetch(
  //     "http://127.0.0.1:8000/api/text/",
  //     {
  //       //results doesn't have anything in the array when printed
  //       headers: {
  //         "Content-Type": "application/json",
  //         Accept: "application/json",
  //         Authorization: "Token " + localStorage.getItem("user"),
  //       },
  //       body: JSON.stringify({
  //         "user" : localStorage.getItem("user")
  //       })
  //     }
  //   );

  //   let q = await response.json();
  // }

  const executeView = async () => {
    // Control validation for Join Workspace inputs
    // user must pass a name and a password.
    if (wsMakeName !== "" && wsMakePassword !== "") {
      setFormValid(true);
    } else {
      setFormValid(false);
    }

    if (formValid) {
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
      //       "name": wsJoinName,
      //       "pass": wsJoinPassword
      //     })
      //   }
      // );
      // Not really sure what this would look like.
      // Would need to contain a
      // 1. ID. integer
      // 2. Owner. String
      // 3. Name. String
      // 4. Tags. List of strings?
      // let q = await response.json();
      // console.log(response);
      // setText(q);
    } else {
      console.log("Error state triggered (VIEW)");
      setErrorState(true);
    }
  };

  const executeCreate = () => {
    if (wsMakeName !== "" && wsMakePassword !== "") {
      setFormValid(true);
    } else {
      setFormValid(false);
    }
    if (formValid) {
      setErrorState(false);
      // fetch("http://127.0.0.1:8000/api/workspaces/", {
      //   // making new workspaces
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     Authorization: "Token " + localStorage.getItem("user"),
      //   },
      //   body: JSON.stringify({
      //     "name": wsMakeName,
      //     "pass": wsMakePassword
      //   })
      // });
      setCreateShow(false);
    } else {
      console.log("Error state triggered (CREATE)");
      setErrorState(true);
    }
  };

  const setFilter = (test) => {
    console.log("e");
    setValue(test);
  };

  const test = (input) => {
    console.log(input.target.title);
  };

  // Handles logout with Github authentication.
  // Right now this is pretty janky as theres no set log out page or anything.
  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  // Used to continuously keep track of what is in the search bar.
  // Ideally, it would need to only be passed once on a query being submitted.
  // TODO: Look into implementing that.
  const handleChange = () => {
    const value = textInput.current.value;
    console.log(value);
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

  // consts for chips (tags)
  // const ListItem = styled("li")(({ theme }) => ({
  //   margin: theme.spacing(0.5),
  // }));

  const [joinShow, setJoinShow] = useState(false);
  const [createShow, setCreateShow] = useState(false);

  //methods for joining a new workspace popup
  const handleShowJoin = () => {
    setJoinShow(true);
  };

  const handleCloseJoin = () => {
    setJoinShow(false);
    setErrorState(false);
  };

  //methods for creating a new workspace popup
  const handleShowCreate = () => {
    setCreateShow(true);
  };

  const handleCloseCreate = () => {
    setCreateShow(false);
    setErrorState(false);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 90 },

    {
      field: "wsOwner",
      headerName: "Owner",
      width: 150,
    },

    {
      field: "wsName",
      headerName: "Name",
      width: 250,

      renderCell: (cellValue) => {
        //cell customization, make the name a link to the corresponding results page
        return (
          <a href={"/workspace/" + cellValue.formattedValue}>
            {cellValue.formattedValue}
          </a>
        );
      },
    },

    {
      field: "wsTags",
      headerName: "Tags",
      flex: 1,
      // renderCell: renderTags
      renderCell: (tag_list) => {
        if (tag_list.formattedValue == null) {
          tag_list = [];
        } else {
          tag_list = tag_list.formattedValue.split(",");
        }

        console.log(tag_list);

        return (
          <Autocomplete
            multiple
            id="tags-filled"
            options={[]}
            defaultValue={tag_list}
            freeSolo
            fullWidth
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  // variant="outlined"
                  label={option}
                  color="primary"
                  {...getTagProps({ index })}
                />
              ))
            }
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                // InputProps={{ disableUnderline: true }}
                label=""
                placeholder="Add Tags"
              />
            )}
          />
        );
      },
    },
  ];

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

        {/* Container for the rest of the contents of the page
        Header, Dropdown Menus, Search Bar and Grid */}
        <Container>
          <div
            className="customRowContainer"
            style={{ paddingBottom: "2%", paddingTop: "1%" }}
          >
            <h2 className="wsHeadingsInternal" style={{ paddingTop: "1%" }}>
              Workspaces
            </h2>
          </div>

          {/* Inline search bar and drop down menu. */}
          {/* <Container> */}
          <Row>
            <div className="customRowContainer">
              {/* Column for Dropdown Menu */}
              {/* TODO:
              Make it so the text changes.
              Implement filtering based on user. */}

              <DropdownButton
                id="dropdown-basic-button"
                title={dropDownValue}
                style={{ float: "left", marginLeft: "0px" }}
              >
                <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                  Workspaces Owned by Me
                </Dropdown.Item>
                <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                  Workspaces Not Owned by Me
                </Dropdown.Item>
                <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                  All Workspaces
                </Dropdown.Item>
              </DropdownButton>

              <div className="DropdownAlignRight">
                <DropdownButton
                  id="dropdown-basic-button"
                  title={dropDownValueSearch}
                  style={{ float: "right", marginLeft: "10px" }}
                  // className="querySelect"
                >
                  <Dropdown.Item
                    onClick={(e) => setDropDownValueSearch(e.target.text)}
                  >
                    Owner
                  </Dropdown.Item>
                  <Dropdown.Item
                    onClick={(e) => setDropDownValueSearch(e.target.text)}
                  >
                    Name
                  </Dropdown.Item>
                  <Dropdown.Item
                    onClick={(e) => setDropDownValueSearch(e.target.text)}
                  >
                    Tags
                  </Dropdown.Item>
                </DropdownButton>
              </div>

              {/* If we want to add a button here with the icon bar this is pretty easy. For now, the user can send input with the search bar. Just add 
                  <Button 
                  variant="light" 
                  type="text"
                  > */}

              <div className="workspaceSearchInternal">
                <Form onSubmit={onSubmitSearch}>
                  <InputGroup>
                    <InputGroup.Text>
                      <Search></Search>
                    </InputGroup.Text>
                    <Form.Control
                      placeholder={"Search by Workspace " + dropDownValueSearch}
                      ref={textInput}
                      onChange={() => handleChange()}
                      type="text"
                    />
                  </InputGroup>
                </Form>
              </div>
            </div>
          </Row>

          {/* </Container> */}

          {/* WORKSPACE TABLE */}
          <Row>
            <div className="customRowContainer">
              <div className="individualTable">
                <Box sx={{ height: 400, width: "100%" }}>
                  <DataGrid
                    rows={fake_data}
                    columns={columns}
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

          {/* New row for add new workspace button. */}
          <Row className="text-center">
            <div className="add-new-button">
              <Button style={{ paddingLeft: 3 }} onClick={handleShowJoin}>
                Join Existing Workspace
              </Button>

              <Button onClick={handleShowCreate}>Create New Workspace</Button>
            </div>
          </Row>

          <Modal show={createShow} onHide={handleCloseCreate}>
            <Modal.Header closeButton onClick={handleCloseCreate}>
              <Modal.Title>Create New Workspace</Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <Form.Control
                type="email"
                placeholder="* Enter Workspace Name"
                onChange={(name) => setMakeName(name.target.value)}
              />
              <Form.Control
                type="email"
                placeholder="* Enter Password"
                onChange={(name) => setMakePassword(name.target.value)}
              />

              <div className="error">
                {errorState ? (
                  <p> ** Please fill in the required forms.</p>
                ) : (
                  <p></p>
                )}
              </div>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-center">
              <Button variant="primary" onClick={executeCreate}>
                Create Workspace
              </Button>
            </Modal.Footer>
          </Modal>

          <Modal show={joinShow} onHide={handleCloseJoin}>
            <Modal.Header closeButton>
              <Modal.Title>Join Workspace</Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <Form.Control
                type="email"
                placeholder="* Enter Workspace Name"
                onChange={(name) => setJoinName(name.target.value)}
              />
              <Form.Control
                type="email"
                placeholder="* Enter Password"
                onChange={(name) => setJoinPassword(name.target.value)}
              />

              <div className="error">
                {errorState ? (
                  <p> ** Please fill in the required forms.</p>
                ) : (
                  <p></p>
                )}
              </div>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-center">
              <Button variant="primary" onClick={executeView}>
                Join Workspace
              </Button>
            </Modal.Footer>
          </Modal>
        </Container>
      </div>
    );
  }
};

export default Workspaces;