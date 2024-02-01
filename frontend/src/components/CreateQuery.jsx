import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/createquery.css";

const CreateQuery = () => {
  const navigate = useNavigate();

  const [queryName, setQueryName] = useState("");
  const [queryDescription, setQueryDescription] = useState("");
  const [primary, setPrimary] = useState("");
  const [secondary, setSecondary] = useState("");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
    //  <a href="/dashboard">Dashboard</a>;
  };

  const [validated, setValidated] = useState(false);

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      event.preventDefault();
      event.stopPropagation();

      var data = {
        name: document.getElementById("nameID").value,
        description: document.getElementById("descriptionID").value,
        keywords: [
          document.getElementById("primaryID").value,
          document.getElementById("secondaryID").value,
        ],
      };

      console.log(JSON.stringify(data));

      fetch("http://127.0.0.1:8000/api/queries/", {
        //submitting a query
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
        body: JSON.stringify(data),
      }); 
      navigate("/queries/");
    }

    setValidated(true);
    console.log(JSON.stringify(data));
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
        <div id="page-wrapper">
          <h2 className="headings">Create Query</h2>
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group controlId="validationCustom01">
            <Form.Label className="formLabels">Query Name *</Form.Label>
            <Form.Control
              type="text"
              placeholder=""
              className="formInputs"
              id="nameID"
              value={queryName}
              onChange={(e) => {
                setQueryName(e.target.value);
              }}
              required
            />
            <Form.Control.Feedback type="invalid" className="formValidation">
              Please provide a query name.
            </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="validationCustom02">
            <Form.Label className="formLabels">Description *</Form.Label>
            <Form.Control
              type="text"
              placeholder=""
              className="formInputs"
              id="descriptionID"
              value={queryDescription}
              onChange={(e) => {
                setQueryDescription(e.target.value);
              }}
              required
            />
            <Form.Control.Feedback type="invalid" className="formValidation">
              Please provide a description.
            </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="validationCustom03">
            <Form.Label className="formLabels">
              Primary Keyword (only 1) *
            </Form.Label>
            <Form.Control
              type="text"
              placeholder=""
              className="formInputs"
              id="primaryID"
              value={primary}
              onChange={(e) => {
                setPrimary(e.target.value);
              }}
              required
            />
            <Form.Control.Feedback type="invalid" className="formValidation">
              Please provide a keyword.
            </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="validationCustom04">
            <Form.Label className="formLabels">
              Secondary Keyword(s) *
            </Form.Label>
            <Form.Control
              type="text"
              placeholder=""
              className="formInputs"
              id="secondaryID"
              value={secondary}
              onChange={(e) => {
                setSecondary(e.target.value);
              }}
              required
            />
            <Form.Control.Feedback type="invalid" className="formValidation">
              Please provide secondary keyword(s).
            </Form.Control.Feedback>
            </Form.Group>
            <div className="centerButtonAlign">
              <Button
                variant="primary"
                className="centerButton"
                type="submit"
              >
                Submit Query
              </Button>
            </div>
          </Form>
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

export default CreateQuery;
