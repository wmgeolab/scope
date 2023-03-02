import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const DisplayArticle = () => {
  //   var { Readability } = require("@mozilla/readability");
  const { article_title } = useParams();
  const [text, setText] = useState("");
  const navigate = useNavigate();
  console.log(article_title)

  const handleSubmit = async (source_id) => {
    let response = await fetch(
      "http://127.0.0.1:8000/api/text/" +
        source_id +
        "/",
      {
        //results doesn't have anything in the array when printed
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      }
    );

    let q = response.body
    setText(q)
    console.log(q)
    
  }

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
    return <div>hello</div>;
  }
};

export default DisplayArticle;
