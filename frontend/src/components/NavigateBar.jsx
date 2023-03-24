import "bootstrap/dist/css/bootstrap.min.css";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

import logo from "./../images/pic10.jpg";

// issue: needs to bring over the github functionality
return (
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
              <Nav.Link href="/" className="nav-elements">Home</Nav.Link>
              <Nav.Link href="queries" className="nav-elements">Queries</Nav.Link>
              <Nav.Link href="workspaces" className="nav-elements">Workspaces</Nav.Link>
              <Container class="ms-auto">
                {login ? (
                  <div style={{ paddingLeft: 100 }}>
                    <Button
                      type="button"
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
                    className="button style1 large"
                    clientId="75729dd8f6e08419c896"
                    onSuccess={handleSubmit}
                    onFailure={onFailure}
                  />
                )}
              </Container>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
);

export default NavigateBar;