import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoginGithub from "react-login-github";
import { AlertTitle, Alert } from "@mui/material/";


import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';


import logo from './../images/pic10.jpg';
import stars from './../images/stars3.jpg';
import "../assets/css/workspace.css";
import { DataGrid } from '@mui/x-data-grid';
import Box from '@mui/material/Box';


const fake_data = [

    {   
        id:0,
        wsOwner:"user1",
        wsName:"workspace1"
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
        wsName:"workspace4"
    }
];

const columns = [

    {field: 'id', headerName:'ID', width:90},

    {
        field: 'wsOwner',
        headerName:"Workspace Owner",
        width:150,
    },

    {
        field: 'wsName',
        headerName:"Workspace Name",
        width:150,
    }

];

const Workspaces = () => {
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
                    <Container class="ms-auto">

                    </Container>
                </Nav>
            </Navbar.Collapse>
        </Container>
        </Navbar>
        <Container>
        <div>
            {/* Heading for text */}
            <h2 className = "headings">Workspaces</h2>
        </div>
        
        {/* Dropdown Menu */}
        <div className = "dropdown">
            
            <label for="dropdown-workspace"></label>
            <select name="dropdown-workspace" id="menu-workspace">

                <option value="yours">Your Workspaces</option>
                <option value="others">Other Workspaces</option>
            </select>
        </div>
        <div>

        <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
        rows={fake_data}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
      />
       </Box>
        </div>
        </Container>
        
    </div>
    )
}

};

export default Workspaces;