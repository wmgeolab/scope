import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoginGithub from "react-login-github";
import { AlertTitle, Alert, Input } from "@mui/material/";

import { Col, Container, Row } from "react-bootstrap";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';


import logo from './../images/pic10.jpg';
import stars from './../images/stars3.jpg';
import 'bootstrap/dist/css/bootstrap.min.css';
import "../assets/css/workspace.css";
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';  
import Form from 'react-bootstrap/Form';  
import { Button } from "react-bootstrap";
import InputGroup from 'react-bootstrap/InputGroup';
import { Search } from 'react-bootstrap-icons';
import { GridToolbar } from '@mui/x-data-grid';

const fake_data = [

    {   
        id:0,
        wsOwner:"user1",
        wsName:"workspace1",
        wsComments:"Argentina:Project"
    },
    {
        id: 1,
        wsOwner:"user2",
        wsName:"workspace2"
    },
    {
        id: 2,
        wsOwner:"user3",
        wsName:"workspace3"
    },
    {
        id: 3,
        wsOwner:"user4",
        wsName:"workspace4",
        wsComments:"Ukraine-Mines"
    }
];

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
        width:150,
    },

    {
        field: 'wsComments',
        headerName:"Comments",
        width:150,
    }

];

const Workspaces = () => {

// Used for the filtering model with the external search bar and the data grid.
const [filt, setFilt] = useState([]);
const [user, setUser] = React.useState('');
const [login, setLogin] = useState(false);

const handleChange = (event) => {
    setUser(event.target.value);
};


const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
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
        <Navbar bg="dark" variant="dark">
        <Container>
            <Navbar.Brand href="/">
                <img
                    src = {logo}
                    width="30"
                    height="30"
                    className="d-inline-block align top"
                    alt="Scope Logo"
                />{' '}
                SCOPE</Navbar.Brand>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                    <Nav.Link href="queries">Queries</Nav.Link>
                    <Nav.Link href="workpaces">Home</Nav.Link>
                    <Container className="ms-auto">

                    {/* TODO: Implement/Discuss a way to handle if a user logs out here. Right now it works
                    but it is very glitchy. */}

                    {/* Log Out button */}
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
        <Row>
        <div>
            <h2 className = "ws_headings">Workspaces</h2>
        </div>
        </Row>
        
        
        {/* Inline search bar and drop down menu. */}
        <Container>
            <Row>



                {/* Column for Dropdown Menu */}
                <Col>
                <div className = "dropDown-WorkSpace">
                <DropdownButton id="dropdown-basic-button" title="All Workspaces">
                    <Dropdown.Item href="#/my-workspaces">Workspaces Owned by Me</Dropdown.Item>
                    <Dropdown.Item href="#/other-workspaces">Workspaces Not Owned by Me</Dropdown.Item>
                    <Dropdown.Item href="#/">All Workspaces</Dropdown.Item>
                </DropdownButton>
                </div>
                </Col>

                
                {/* Column for Search Bar    */}
                <Col>
                <div className = "workspaceSearch">
                <Form>  
                    <InputGroup>
                    <InputGroup.Text>
                     <Search></Search>
                    </InputGroup.Text>
                    <Form.Control type="text" 
                    placeholder="Search by Keyword" />
                    </InputGroup>
                </Form>           
                </div>
                </Col>

            </Row>
 

        {/* TODO: Change this to a bootstrap2 datagrid and clean the code up. */}

        <Row>
            <div className = "table">
            <Box sx={{ height: 400, width: '100%' }}>
            <DataGrid
                rows={fake_data}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                checkboxSelection
                disableSelectionOnClick
                experimentalFeatures={{ newEditingApi: true}}
                components={{ Toolbar: GridToolbar }}
                filterModel={{
                    items:filt
                }}
            />
          </Box>
          </div>
        </Row>
        </Container>

 

        
        {/* New row for add new workspace button. */}
        <Row className = "text-center">
            <div className ="add-new-button">
                <Button href="#/new_workspace_page">Add New Workspace</Button>
            </div>    
        </Row> 

        


        
        </Container>


    </div>
    )
}

};

export default Workspaces;