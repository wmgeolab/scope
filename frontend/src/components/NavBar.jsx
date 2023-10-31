import React, { useState } from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";

const NavBar = () => {
    
    const navigate = useNavigate();
    
    const handleLogout = () => {
        localStorage.clear();
        navigate("/");
        //  <a href="/dashboard">Dashboard</a>;
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
                    <Nav.Link href="queries" className="nav-elements">
                      Queries
                    </Nav.Link>
                    <Nav.Link href="workspaces" className="nav-elements">
                      Workspaces
                    </Nav.Link>
                    <Container className="ms-auto">
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
            </div>
        )
        }
}

export default NavBar;