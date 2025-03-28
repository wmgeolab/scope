import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container } from "react-bootstrap";
import UnauthorizedView from "../UnauthorizedView";
import { API } from "../../api/api";

const DisplayArticle = (props) => {
  const { loggedIn } = props;
  //   var { Readability } = require("@mozilla/readability");
  const { article_title } = useParams();
  const [text, setText] = useState("");
  console.log(article_title);

  const handleSubmit = useCallback(async (source_id) => {
    let response = await fetch(
      API.url(`/api/text/${source_id}/`),
      {
        headers: API.getAuthHeaders(),
      }
    );

    let q = await response.text();
    console.log(response);

    setText(q);
  }, [setText]);

  useEffect(() => {
    handleSubmit(article_title);
  }, [article_title, handleSubmit]); //adding article_title to dependency array

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
