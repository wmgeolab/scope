import React from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";

export default function individualWorkspaceQuestionModal(props) {
    const { showModal, handleClose, workspaceName } = props;

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
        <Form.Label>Question 1</Form.Label>
        <Form.Control type="email" placeholder="Existing LLM Response" />
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Question 2</Form.Label>
        <Form.Control type="email" placeholder="Existing LLM Response" />
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Question 3</Form.Label>
        <Form.Control type="email" placeholder="Existing LLM Response" />
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Question 4</Form.Label>
        <Form.Control type="email" placeholder="Existing LLM Response" />
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
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