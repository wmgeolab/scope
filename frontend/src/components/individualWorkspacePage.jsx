import { useParams } from "react-router-dom";
import React, { useState, useRef, useEffect } from "react";
import { Row, Button, Col, Form, InputGroup } from "react-bootstrap";
import { Container } from "@mui/material";
import { Search } from "react-bootstrap-icons";
import UnauthorizedView from "./UnauthorizedView";
import IndividualWorkspaceTable from "./IndividualWorkspaceTable";
import IndividualWorkspaceModal from "./IndividualWorkspaceModal";

export default function IndividualWorkspacePage(props) {
  const { loggedIn } = props;
  const { workspace_name } = useParams();
  const [showModal, setShowModal] = useState(false);
  const [filters, setFilters] = useState([]);
  const textInput = useRef("");

  const handleCloseModal = () => {
    setShowModal(false);
  };
  const handleShowModal = () => {
    setShowModal(true);
  };

  const handleKeywordChange = (value) => {
    textInput.current = value.target.value;
  };

  const onSubmitSearch = () => {
    setFilters([
      {
        columnField: "wsName",
        operatorValue: "contains",
        value: textInput.current,
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
                <Button aria-label="Search" onClick={onSubmitSearch}>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-search"
                    viewBox="0 0 16 16"
                  >
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                  </svg>
                </Button>
                <Form.Control
                  placeholder="Search by Article Name"
                  ref={textInput}
                  onChange={handleKeywordChange}
                  type="text"
                />
              </InputGroup>
            </Form>
          </Col>
        </Row>
        <IndividualWorkspaceTable data={data} filters={filters} />
        <Row className="mt-5">
          <Col sm={5}/>
          <Col sm={2}>
            <Button onClick={handleShowModal}>Share Workspace</Button>
          </Col>
          <Col sm={5}/>
        </Row>
        <IndividualWorkspaceModal 
          showModal={showModal}
          handleCloseModal={handleCloseModal}
          workspaceName={workspace_name}
        />
      </Container>
    );
  }
}
