import React, { useState, setState } from "react";
import { useNavigate } from "react-router-dom";

import { Col, Container, Row } from "react-bootstrap";
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
import { styled } from '@mui/material/styles';
import Chip from '@mui/material/Chip';
import Paper from '@mui/material/Paper';


const fake_data = [
    {   
        id:0,
        wsOwner:"user1",
        wsName:"My Workspace 1",
        wsTags:"Argentina"
    },
    {
        id: 1,
        wsOwner:"user2",
        wsName:"My Workspace 2"
    },
    {
        id: 2,
        wsOwner:"user3",
        wsName:"My Workspace 3",
        wsTags: "please,help"
    },
    {
        id: 3,
        wsOwner:"user4",
        wsName:"My Workspace 4",
        wsTags:"Ukraine"
    }
];

const Workspaces = () => {

// Used for the filtering model with the external search bar and the data grid.
const [filt, setFilt] = useState([]);
const navigate = useNavigate();
var textInput = React.createRef(); 
var [dropDownValue,setValue] = useState('All Workspaces');


  const setFilter = (test) => {
    //console.log(this.input.value);
    //console.log("????");
    // this works
    //console.log(test.target.text);
    setValue(test.target.text);
  };

  const test = (input) => {
    //console.log("...");
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
    // console.log(value);
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
          value: textInput.current.value
        }
       ])
};

// consts for chips (tags)
const ListItem = styled('li')(({ theme }) => ({
    margin: theme.spacing(0.5),
}));
  
const handleClickChip = () => {
    
};

const handleDeleteChip = (tagToDelete) => {

};

const columns = [

    {field: 'id', headerName:'ID', width:90},

    {
        field: 'wsOwner',
        headerName:"Owner",
        width:150,
    },

    {
        field: 'wsName',
        headerName:"Name",
        width:250,
        renderCell: (cellValue) => {
            //cell customization, make the name a link to the corresponding results page
            return <a href={"/workspace/" + cellValue.formattedValue}>{cellValue.formattedValue}</a>;
          }
    },

    {
        field: 'wsTags',
        headerName:"Tags",
        flex:1,
        // renderCell: renderTags
        renderCell: (params) => {
            if(params.formattedValue == null) {
                params = []
            }
            else {
                params = params.formattedValue.split(",")
            }
                
            return <Paper elevation={0}
                sx={{
                display: 'flex',
                justifyContent: 'center',
                flexWrap: 'wrap',
                listStyle: 'none',
                p: 0.5,
                m: 0,
                backgroundColor: 'transparent'
                }}
                component="ul"
            >
                
                {params.map((params) => {
                    return (
                        <ListItem key={params}>
                        <Chip
                            label={params}
                            onDelete={handleDeleteChip(params)}
                        />
                        </ListItem>
                        
                    );
                })}
                <ListItem>
                    <Chip label="+" onClick={handleClickChip} />
                </ListItem>
                
            </Paper>
        }
    }

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
          <Container>
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
                  onClick={(e) => test(e)}
                >
                  <Dropdown.Item onClick={(e) => setFilter(e)}>
                    Workspaces Owned by Me
                  </Dropdown.Item>
                  <Dropdown.Item onClick={(e) => setFilter(e)}>
                    Workspaces Not Owned by Me
                  </Dropdown.Item>
                  <Dropdown.Item onClick={(e) => setFilter(e)}>
                    All Workspaces
                  </Dropdown.Item>
                </DropdownButton>

                {/* If we want to add a button here with the icon bar this is pretty easy. For now, the user can send input with the search bar. Just add 
                    <Button 
                    variant="light" 
                    type="text"
                    > */}

                {/* Column for Search Bar    */}
                <Col>
                  <div className="workspaceSearchInternal">
                    <Form onSubmit={onSubmitSearch}>
                      <InputGroup>
                        <InputGroup.Text>
                          <Search></Search>
                        </InputGroup.Text>
                        <Form.Control
                          placeholder="Search by Workspace Name"
                          ref={textInput}
                          onChange={() => handleChange()}
                          type="text"
                        />
                      </InputGroup>
                    </Form>
                  </div>
                </Col>
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
              <Button href="#/new_workspace_page">Add New Workspace</Button>
            </div>
          </Row>
        </Container>
      </div>
    );
  }
};

export default Workspaces;