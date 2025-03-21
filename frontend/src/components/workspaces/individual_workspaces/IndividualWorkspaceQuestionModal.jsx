import React from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";

export default function individualWorkspaceQuestionModal(props) {
    const { workspaceQuestions, showModal, handleClose, workspaceName } = props;

//   const handleCopyClick = (text) => {
//     navigator.clipboard.writeText(text)
//     .then(() => {
//       console.log("Text copied to clipboard:", text);
//     })
//     .catch((error) => {
//       console.error("Error copying text to clipboard:", error);
//     });
//   }; 

  return(
  <Modal show={showModal} onHide={handleClose}>
    <Modal.Header closeButton>
      <Modal.Title>Add Workspace Questions</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      {/* <Form.Control
            type="email"
            placeholder="* Enter Question"
          //   onChange={(name) => setTempWorkspaceName(name.target.value)}
      /> */}
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Location Question</Form.Label>
        <Form.Control as="textarea" rows={3} placeholder={workspaceQuestions[0] ? workspaceQuestions[0].question : 'No existing question'} />
        <Form.Control as="textarea" rows={3} placeholder="Existing LLM Response" />
        <div className="d-grid gap-2">
          <Button variant="secondary">
            Edit Response
          </Button>
        </div>
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Date/Time Question</Form.Label>
        <Form.Control as="textarea" rows={3} placeholder={workspaceQuestions[1] ? workspaceQuestions[1].question : 'No existing question'} />
        <Form.Control as="textarea" rows={3} placeholder="Existing LLM Response" />
        <div className="d-grid gap-2">
          <Button variant="secondary">
            Edit Response
          </Button>
        </div>
        <Form.Text className="text-muted">
          Enter any questions related to the date/time of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Actors Question</Form.Label>
        <Form.Control as="textarea" rows={3} placeholder={workspaceQuestions[2] ? workspaceQuestions[2].question : 'No existing question'} />
        <Form.Control as="textarea" rows={3} placeholder="Existing LLM Response" />
        <div className="d-grid gap-2">
          <Button variant="secondary">
            Edit Response
          </Button>
        </div>
        <Form.Text className="text-muted">
          Enter any questions related to the actors present in an article.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Summary Question</Form.Label>
        <Form.Control as="textarea" rows={3} placeholder={workspaceQuestions[3] ? workspaceQuestions[3].question : 'No existing question'} />
        <Form.Control as="textarea" rows={3} placeholder="Existing LLM Response" />
        <div className="d-grid gap-2">
          <Button variant="secondary">
            Edit Response
          </Button>
        </div>
        <Form.Text className="text-muted">
          Enter any questions related to the summarizing the article.
        </Form.Text>
      </Form.Group>
          
      {/* <Form.Control
            type="email"
            placeholder="* Enter Question"
          //   onChange={(name) => setTempWorkspacePassword(name.target.value)}
      /> */}
    </Modal.Body>
    <Modal.Footer className="d-flex justify-content-center">
      <Button variant="primary">
        Apply To Workspace
      </Button>
    </Modal.Footer>
  </Modal>);
}