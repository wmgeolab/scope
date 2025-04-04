import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Row, Button, Col, Form, InputGroup } from "react-bootstrap";
import { Container } from "@mui/material";
import { Search } from "react-bootstrap-icons";
import UnauthorizedView from "../../UnauthorizedView";
import IndividualWorkspaceTable from "./IndividualWorkspaceTable";
import IndividualWorkspaceModal from "./IndividualWorkspaceModal";
import IndividualWorkspaceQuestionModal from "./IndividualWorkspaceQuestionModal";
import { API } from "../../../api/api";


export default function IndividualWorkspacePage(props) {
  const { loggedIn } = props;
  const { workspace_name, workspace_id } = useParams();
  // showModal is not unused -- just only 
  // const [showModal, setShowModal] = useState(false);

  const [showQuestionModal, setShowQuestionModal] = useState(false);
  const [showWorkspaceModal, setShowWorkspaceModal] = useState(false);

  const [workspaceSources, setWorkspaceSources] = useState([]);
  const [workspaceQuestions, setWorkspaceQuestions] = useState([]);
  //const [workspaceResponses, setWorkspaceResponses] = useState([]);

  var textInput = React.createRef();
  const [filt, setFilt] = useState([]);

  const handleCloseModal = () => {
    setShowWorkspaceModal(false);
  };
  const handleCloseQuestionModal = async () => {
    setShowQuestionModal(false);
    await obtainQuestions();
    //await obtainResponses();
  };

  const handleShowModal = () => {
    setShowWorkspaceModal(true);
  };

  const handleShowQuestionModal = () => {
    setShowQuestionModal(true);
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

  async function obtainSources() {
    const param = new URLSearchParams({
      workspace: workspace_id
    })
    console.log('Workspace ID: ', workspace_id);
    const response = await fetch(API.url(`/api/entries/?${param}`), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });

    const response_text = await response.json();

    const formattedResponse = response_text.results.map(result => {
      return {
        id: result.source.id,
        wsName: result.source.text,
        wsURL: result.source.url,
      }
    });

    if (formattedResponse)
      setWorkspaceSources(formattedResponse);
  }

  // Gets all paginated questions
  async function obtainQuestions() {
    const param = new URLSearchParams({
      workspace: workspace_id
    })

    let allResults = [];
    let nextUrl = API.url(`/api/questions/?${param}`);

    while(nextUrl) {
      console.log("nextUrl value: ", nextUrl);
      // const response = await fetch(nextUrl, {
      //   method: "GET",
      //   headers: {
      //     "Content-Type": "application/json",
      //     Authorization: "Token " + localStorage.getItem("user"),
      //   },
      // });
      const response = await fetch(nextUrl, {
        method: "GET",
        headers: API.getAuthHeaders(),
      });

      const response_text = await response.json();

      // JUST FOR TESTING
      console.log("Raw Questions Response: ", response_text);

      const formattedResponse = response_text.results.map(result => {
        return {
          id: result.id,
          question: result.question,
        }
      });

      allResults = [...allResults, ...formattedResponse];
      nextUrl = response_text.next;
    }

    setWorkspaceQuestions(allResults);

    // const response = await fetch(API.url(`/api/questions/?${param}`), {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //     Authorization: "Token " + localStorage.getItem("user"),
    //   },
    // });

    // const response_text = await response.json();

    // // JUST FOR TESTING
    // console.log("Raw Questions Response:\n");
    // console.log(response_text);

    // const formattedResponse = response_text.results.map(result => {
    //   return {
    //     id: result.id,
    //     question: result.question,
    //   }
    // });

    // if (formattedResponse)
    //   setWorkspaceQuestions(formattedResponse);
  }

  // async function obtainResponses() {
  //   const param = new URLSearchParams({
  //     workspace: workspace_id
  //   })
  //   const response = await fetch(API.url(`/api/ai_responses/?${param}`), {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: "Token " + localStorage.getItem("user"),
  //     },
  //   });

  //   const response_text = await response.json();

  //   // JUST FOR TESTING
  //   console.log("Raw Responses Array:");
  //   console.log(response_text);

  //   const formattedResponse = response_text.results.map(result => {
  //     return {
  //       id: result.id,
  //       summary: result.summary,
  //       entities: result.entities,
  //       locations: result.locations,
  //       source_id: result.source.id,
  //       workspace_id: result.workspace
  //     }
  //   });

  //   if (formattedResponse)
  //     setWorkspaceResponses(formattedResponse);
  // }

  //console.log('WS ID: ', workspace_id);

  useEffect(() => {
    obtainSources();
    obtainQuestions();
    //obtainResponses();
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
        <IndividualWorkspaceTable data={workspaceSources} filt={filt} workspace_id={workspace_id} />
        <Row className="mt-5">
          <Col sm={4} />
          <Col sm={2}>
            <Button onClick={handleShowQuestionModal}>Set Questions</Button>
          </Col>
          <Col sm={2}>
            <Button onClick={handleShowModal}>Share Workspace</Button>
          </Col>
        </Row>
        <IndividualWorkspaceModal
          showModal={showWorkspaceModal}
          handleClose={handleCloseModal}
          workspaceName={workspace_name}
        />{showQuestionModal &&
          <IndividualWorkspaceQuestionModal
            workspaceQuestions={workspaceQuestions}
            showModal={showQuestionModal}
            handleClose={handleCloseQuestionModal}
            workspace_id={workspace_id}
          />}
      </Container>
    );
  }
}