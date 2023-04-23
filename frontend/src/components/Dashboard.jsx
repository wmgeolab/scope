import React, { useState, useEffect } from "react";
import "../assets/css/dashboard.css";
import "bootstrap/dist/css/bootstrap.min.css";
import LoginGithub from "react-login-github";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import stars from "./../images/stars3.jpg";
import create from "./../images/icons/create_queries.png";
import filter from "./../images/icons/filtering_queries.png";
import workspaces from "./../images/icons/workspaces.png";

const Dashboard = () => {
  const onFailure = (response) => console.error(response);

  const [login, setLogin] = useState(false); //keep track of if a user is logged in

  //runs once when page is refreshed, checks if a user is already logged in (persistent login)
  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    console.log(loggedInUser);
    if (loggedInUser) {
      setLogin(true);
    }
  }, []);

  //retrieve the user token from the backend
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

  //clears the user token from local storage to "log out" the user
  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
  };

  return (
    <div>
      <Navbar bg="dark" variant="dark" className="nav">
        <Container>
          <Navbar.Brand className="nav-title">
            <img
              src={logo}
              width="30"
              height="30"
              className="d-inline-block align-top padding"
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
                {login ? (
                  <div style={{ paddingLeft: 100 }}>
                    <Button
                      type="button"
                      // variant='login'
                      className="login"
                      onClick={handleLogout}
                      style={{ justifyContent: "right" }}
                      size="xs"
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

      <div
        style={{
          backgroundImage: `url(${stars})`,
          // height: '24em',
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }}
      >
        <h1 className="header">
          <img src={logo} width="100" height="100" alt="Scope logo" /> SCOPE
        </h1>
      </div>
      <h2 className="headings">What is SCOPE?</h2>
      <p className="paragraphs">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras cursus
        ante posuere, congue nunc id, elementum purus. Integer tortor odio,
        luctus accumsan leo quis, posuere finibus orci. Maecenas lobortis justo
        eu ornare pharetra. Proin blandit ipsum at ante commodo, a maximus justo
        placerat. Maecenas commodo velit quam, in bibendum turpis bibendum a.
        Aenean ac enim sit amet est rutrum dignissim. Mauris tempor massa arcu,
        ut porttitor erat ornare scelerisque. Curabitur tempor bibendum tortor,
        at pretium magna suscipit in. Sed molestie interdum sapien, at rhoncus
        est laoreet sit amet. Donec dapibus ligula et rutrum elementum. Integer
        congue at neque ut vulputate. Morbi et arcu ut justo ornare porttitor
        sit amet in enim.
      </p>
      <div></div>
      <h2 className="headings">How to use SCOPE</h2>

      <h3 className="headings2">
        {" "}
        <img src={create} width="50" height="50" alt="create" /> &nbsp; Creating
        Queries
      </h3>
      <p className="paragraphs">
        Cras semper purus at eros euismod facilisis. Maecenas nec risus nulla.
        Curabitur id arcu ante. Praesent pretium, odio sit amet vulputate
        ultrices, nunc ligula malesuada est, ac feugiat ex lorem sit amet
        tortor. In nec dolor ligula. Donec vel arcu nisi. Nam congue neque ac
        massa molestie dignissim. Aenean gravida massa non leo faucibus
        tincidunt.{" "}
      </p>

      <p className="paragraphs_end">
        Donec lectus lectus, tempus id aliquam sed, ultrices eget libero.
        Suspendisse hendrerit sed eros et mollis. Nullam congue, odio et
        malesuada efficitur, lectus est sollicitudin metus, eu vestibulum erat
        quam ut massa. Integer enim nulla, vulputate eget enim ac, scelerisque
        fermentum mauris. Cras et viverra eros, tempor consectetur nisl.
      </p>

      <h3 className="headings2">
        {" "}
        <img src={filter} width="50" height="50" alt="filter" /> &nbsp;
        Filtering Queries
      </h3>
      <p className="paragraphs">
        Cras justo mauris, fringilla id luctus quis, dapibus sit amet eros.
        Nulla nec quam eget felis facilisis euismod. Etiam sollicitudin arcu
        metus, a scelerisque mi blandit sed. Integer placerat feugiat dignissim.
        Morbi et mi et mi lobortis efficitur ut id tellus.
      </p>

      <p className="paragraphs_end">
        Aliquam fermentum faucibus metus porta vulputate. Nunc ultrices volutpat
        risus tristique convallis.
      </p>

      <h3 className="headings2">
        {" "}
        <img src={workspaces} width="50" height="50" alt="workspaces" /> &nbsp;
        Using Workspaces
      </h3>

      <p className="paragraphs_end">
        Fusce posuere porta metus. Curabitur vitae dictum odio, sit amet
        malesuada leo. Fusce ut consequat dolor. Nulla nec erat finibus libero
        gravida faucibus a sit amet turpis. Ut volutpat nisi et odio fermentum,
        quis facilisis arcu pellentesque. Nullam vel rhoncus metus, in tempor
        tortor. Praesent mollis vel quam et dapibus. Cras vel neque non dolor
        interdum iaculis. Nulla facilisi. Donec aliquet tincidunt eros, eu porta
        nisl. Praesent nec tortor quis mauris laoreet aliquet quis a libero.
      </p>

      <div className="footnote">William & Mary geoDev</div>
    </div>
  );
};

export default Dashboard;
