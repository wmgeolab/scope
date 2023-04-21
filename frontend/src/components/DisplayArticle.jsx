import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import { Col, Container, Row } from "react-bootstrap";
import logo from './../images/pic10.jpg';
import Nav from 'react-bootstrap/Nav';
import { Button } from "react-bootstrap";

const DisplayArticle = () => {
  //   var { Readability } = require("@mozilla/readability");
  const { article_title } = useParams();
  const [text, setText] = useState("");
  const navigate = useNavigate();
  const [login, setLogin] = useState(false);
  console.log(article_title)

  const handleSubmit = async (source_id) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/text/" +
        source_id +
        "/",
      {
        //results doesn't have anything in the array when printed
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );

    
    let q = await response.text();
    console.log(response);
   
    setText(q);
   
    
  }

  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
  };

  useEffect(() => {
    handleSubmit(article_title);
  }, []); //listening on an empty array

  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      
      <div>

        <h1>401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
        your access, please return to the <a href="/">dashboard</a> to log in
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
  } else {
    return <div>
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
                    <Nav.Link href="/queries">Queries</Nav.Link>
                    <Nav.Link href="workpace">Workspaces</Nav.Link>
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
        <Container> 
        <h2 className="wsHeadingsInternal" style={{ paddingTop: "1%" }}>
              Article Text:
        </h2>

       
          <div>          
          {text} 
          </div> 
        </Container> 
          
    </div>;
  }
};

export default DisplayArticle;
