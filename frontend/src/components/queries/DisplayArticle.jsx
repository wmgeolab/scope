import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container } from "react-bootstrap";
import UnauthorizedView from "../UnauthorizedView";

const DisplayArticle = (props) => {
  const { loggedIn } = props;
  //   var { Readability } = require("@mozilla/readability");
  const { article_title } = useParams();
  const [text, setText] = useState("");
  console.log(article_title);

  const handleSubmit = async (source_id) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/text/" + source_id + "/",
      {
        //results doesn't have anything in the array when printed
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );

    let q = await response.text();
    console.log(response);

    setText(q);
  };

  useEffect(() => {
    handleSubmit(article_title);
  }, []); //listening on an empty array

  if (loggedIn === false) {
    // fix?
    return <UnauthorizedView />;
  } else {
    return (
      <div>
        <Container>
          <h2 className="wsHeadingsInternal" style={{ paddingTop: "1%" }}>
            Article Text:
          </h2>

          <div>{text}</div>
        </Container>
      </div>
    );
  }
};

export default DisplayArticle;
