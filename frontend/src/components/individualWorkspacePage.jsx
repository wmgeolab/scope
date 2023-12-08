import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Row, Button, Col, Form, InputGroup } from "react-bootstrap";
import { Container } from "@mui/material";
import { Search } from "react-bootstrap-icons";
import UnauthorizedView from "./UnauthorizedView";
import IndividualWorkspaceTable from "./IndividualWorkspaceTable";

export default function IndividualWorkspacePage(props) {
  const { loggedIn } = props;
  const { workspace_name, workspace_id } = useParams();
  const [showModal, setShowModal] = useState(false);

  var textInput = React.createRef();
  const [filt, setFilt] = useState([]);

  const handleCloseModal = () => {
    setShowModal(false);
  };
  const handleShowModal = () => {
    setShowModal(true);
  };

  const onSubmitSearch = (event) => {
    event.preventDefault();
    console.log(
      "The input string being passed here is: ",
      textInput.current.value
    );

    setFilt([
      {
        columnField: "wsName",
        operatorValue: "contains",
        value: textInput.current.value,
      },
    ]);
  };

  const data = [
    {
      id: 0,

      wsName: "article1",
      wsComments: "Argentina:Project",
      wsURL:
        "https://www.cbsnews.com/news/syria-airstrike-us-contractor-killed-iran-drone-attack-joe-biden-lloyd-austin/",
    },
    {
      id: 1,

      wsName: "article2",
      wsURL:
        "https://www.washingtonpost.com/world/2023/03/24/rwanda-rusesabagina-release/",
    },
    {
      id: 2,
      wsName: "article3",
      wsURL:
        "https://www.politico.com/news/2023/03/24/democrats-tiktok-ban-china-00088659",
    },
    {
      id: 3,
      wsName: "article4",
      wsURL:
        "https://www.nytimes.com/2023/03/24/us/politics/house-approves-bill-requiring-schools-to-give-parents-more-information.html",
    },
  ];

  async function obtainSources() {
    const response = await fetch("http://127.0.0.1:8000/api/entries/?workspace=" + workspace_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });

    console.log(response)

    const response_text = await response.json();

    console.log("Response:", response_text);
  }

  useEffect(() => {
    obtainSources();
  }, []);

  if (loggedIn === false) {
    return <UnauthorizedView />;
  } else {
    return (
      <Container>
        <Row className="mt-5">
          <Col sm={1}>
            <Button
              variant="link"
              href="/workspaces"
              style={{
                color: "rgb(48, 46, 46)",
              }}
            >
              🡸 Return home
            </Button>
          </Col>
          <Col sm={4} className="text-start">
            <h1>
              <b>{workspace_name}</b>
            </h1>
          </Col>
          <Col sm={3} />
          <Col sm={4} className="float-end mt-2">
            <Form onSubmit={onSubmitSearch}>
              <InputGroup>
                <InputGroup.Text>
                  <Search></Search>
                </InputGroup.Text>
                <Form.Control
                  placeholder="Search by Article Name"
                  ref={textInput}
                  onChange={null}
                  type="text"
                />
              </InputGroup>
            </Form>
          </Col>
        </Row>
        <IndividualWorkspaceTable data={data} filt={filt}/>
        <Row className="mt-5">
          <Col sm={5}/>
          <Col sm={2}>
            <Button onClick={handleShowModal}>Share Workspace</Button>
          </Col>
          <Col sm={5}/>
        </Row>
      </Container>
    );
  }
}
