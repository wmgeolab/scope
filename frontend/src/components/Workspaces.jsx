import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert } from "@mui/material/";
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';


const Workspaces = () => {

  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const myWorkspaces = (event) => {
    var Button = document.getElementById("demo-button");
    Button.textContent = "My Workspaces";
    handleClose();
  }
  
  const otherWorkspaces = (event) => {
    var Button = document.getElementById("demo-button");
    Button.textContent = "Other Workspaces";
    handleClose();
  }

  const handleClose = () => {
    setAnchorEl(null);
  };
  
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
      <link rel="stylesheet" href="assets/css/table.css" />
      <link rel="stylesheet" href="assets/css/main.css" />
      <div id="page-wrapper">
        {/* <!-- Header --> */}
        <section id="header" className="wrapper">
          {/* <!-- Logo --> */}
          <div id="logo">
            <h1>
              SCOPE
            </h1>
          </div>

          {/* <!-- Nav --> */}
          <nav id="nav">
            <ul>
              {/* <li><a href="left-sidebar.html">Left Sidebar</a></li> */}
              {/* <li><a href="right-sidebar.html">Right Sidebar</a></li> */}
              {/* <li><a href="no-sidebar.html">No Sidebar</a></li> */}
              <li>
                <a href="/">My Workspaces</a>
              </li>
              <li className="current">
                <a href="/workspaces">Workspaces</a>
              </li>
              {/* <li><a href='/login'>Login</a></li> */}
            </ul>
          </nav>
        </section>

        {/* <!-- Main --> */}
        <section id="main" className="wrapper style2">
          <div className="title">Workspaces</div>

          {/* {console.log(queries)} */}
          <div className="container">
            {/* <!-- Features --> */}

            <section id="features">
              <div>
      <Button
        id="demo-button"
        aria-controls={open ? 'demo-positioned-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        My Workspaces
      </Button>
      <Menu
        id="demo-positioned-menu"
        aria-labelledby="demo-positioned-button"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
      > 

        
        <MenuItem onClick={myWorkspaces}>My Workspaces</MenuItem>
        <MenuItem onClick={otherWorkspaces}>Other Workspaces</MenuItem>
      </Menu>
    </div>
            </section>
          </div>
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

export default Workspaces;
