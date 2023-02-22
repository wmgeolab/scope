import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert } from "@mui/material/";
import { styled, alpha } from "@mui/material/styles";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import ListItemText from "@mui/material/ListItemText";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import FolderIcon from "@mui/icons-material/Folder";
import DeleteIcon from "@mui/icons-material/Delete";
import ListItemButton from "@mui/material/ListItemButton";

// to do move this to a style sheet this is
const styles = {
  menu: {
    textAlign: "right",
  },

  rectangle: {
    width: "400px",
    height: "100px",
    background: "blue",
  },
};
const StyledMenu = styled((props) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: "bottom",
      horizontal: "right",
    }}
    transformOrigin={{
      vertical: "top",
      horizontal: "right",
    }}
    {...props}
  />
))(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color:
      theme.palette.mode === "light"
        ? "rgb(55, 65, 81)"
        : theme.palette.grey[300],
    boxShadow:
      "rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px",
    "& .MuiMenu-list": {
      padding: "4px 0",
    },
    "& .MuiMenuItem-root": {
      "& .MuiSvgIcon-root": {
        fontSize: 18,
        position: "relative",
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
      },
      "&:active": {
        backgroundColor: alpha(
          theme.palette.primary.main,
          theme.palette.action.selectedOpacity
        ),
      },
    },
  },
}));

function generate(element) {
  return [0, 1, 2].map((value) =>
    React.cloneElement(element, {
      key: value,
    })
  );
}

const Workspaces = () => {
  var filters = {};

  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const myWorkspaces = (event) => {
    var Button = document.getElementById("demo-button");
    Button.textContent = "My Workspaces";

    var box = document.getElementById("displayBox");
    box.backgroundColor = "red";
    // TODO: Something with fitlers

    handleClose();
  };

  const otherWorkspaces = (event) => {
    var Button = document.getElementById("demo-button");
    Button.textContent = "Other Workspaces";

    var box = document.getElementById("displayBox");
    var box = document.getElementById("displayBox");
    box.backgroundColor = "red";

    // TODO: Something with filters

    handleClose();
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  if (localStorage.getItem("user") === null) {
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
              <h1>SCOPE</h1>
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
                <div class="search-form">
                  <Box id="big-box">
                    <Box id="new-workspace"
                    textAlign="right">
                    <Button 
                    variant="contained"
                    id="new_workspace_button"
                    >
                      Add New Workspace 
                    </Button>

                    </Box>
                    <TextField
                      id="search-bar"
                      label="Keyword Search"
                      variant="filled"
                    />
                    <Button variant="contained">
                      Search Titles By Keyword
                    </Button>
                    <div>
                      <Button
                        id="demo-button"
                        aria-controls={
                          open ? "demo-positioned-menu" : undefined
                        }
                        aria-haspopup="true"
                        aria-expanded={open ? "true" : undefined}
                        onClick={handleClick}
                      >
                        My Workspaces
                      </Button>
                      <StyledMenu
                        id="demo-positioned-menu"
                        aria-labelledby="demo-positioned-button"
                        anchorEl={anchorEl}
                        open={open}
                        onClose={handleClose}
                       
                        anchorOrigin={{
                          vertical: "top",
                          horizontal: "left",
                        }}
                        transformOrigin={{
                          vertical: "top",
                          horizontal: "left",
                        }}
                      >
                        <MenuItem onClick={myWorkspaces}>
                          My Workspaces
                        </MenuItem>
                        <MenuItem onClick={otherWorkspaces}>
                          Other Workspaces
                        </MenuItem>
                      </StyledMenu>
                    </div>
                  </Box>
                </div>

                <Box
                  id="displayBox"
                  sx={{
                    width: "px",
                    height: "400px",
                    border: 3,
                  }}
                >
                  <List>
                    {generate(
                      <ListItem
                        secondaryAction={
                          <IconButton
                            edge="end"
                            aria-label="delete"
                            size="small"
                          >
                            <DeleteIcon />
                          </IconButton>
                        }
                      >
                        <ListItemAvatar>
                          <Avatar>
                            <FolderIcon />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemButton primary="Single-line item">
                          <ListItemText primary="Spam" />
                        </ListItemButton>
                      </ListItem>
                    )}
                  </List>
                </Box>
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
