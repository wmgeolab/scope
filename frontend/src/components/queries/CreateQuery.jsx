import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import "../../assets/css/createquery.css";
import UnauthorizedView from "../UnauthorizedView";

const CreateQuery = (props) => {
  const { loggedIn } = props;
  const navigate = useNavigate();

  const [queryName, setQueryName] = useState("");
  const [queryDescription, setQueryDescription] = useState("");
  const [primary, setPrimary] = useState("");
  const [secondary, setSecondary] = useState("");

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

  if (loggedIn === false) {
    // fix?
    return <UnauthorizedView />;
  } else {
    return (
      <div>
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
