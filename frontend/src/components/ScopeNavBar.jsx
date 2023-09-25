import React, { useState, useEffect } from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import LoginGithub from "react-login-github";

export default function ScopeNavBar(props) {


  const [login, setLogin] = useState(false); //keep track of if a user is logged in
  const { loggedIn } = props;

  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };
  let handleLogin;
  let onFailure;

  if (loggedIn) {

    useEffect(() => {
      const loggedInUser = localStorage.getItem("user");
      console.log(loggedInUser);
      if (loggedInUser) {
        setLogin(true);
      }
    }, []);

    const handleLogin = async (e) => {
      console.log(e.code);
      let token = await fetch("http://127.0.0.1:8000/dj-rest-auth/github", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: e.code }),
      });
      token.json().then((res) => {
        console.log(res);
        localStorage.setItem("user", res.key); //store the user in local storage for persistent login
        setLogin(true);
      });
    };
    const onFailure = (response) => console.error(response);
  }

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
                {login ? (
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
                ) : (
                  <LoginGithub //github gives back code give to backend, backend has client id and client secret (never transmit the secret)
                    className="moduleLogin"
                    clientId="75729dd8f6e08419c896"
                    onSuccess={handleLogin}
                    onFailure={onFailure}
                  />
                )}
              </Container>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}