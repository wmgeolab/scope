import React from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

export default function IndividualWorkspaceModal(props) {
  const { showModal, handleClose, workspaceName } = props;

  const handleCopyClick = (text) => {
    navigator.clipboard.writeText(text)
    .then(() => {
      console.log("Text copied to clipboard:", text);
    })
    .catch((error) => {
      console.error("Error copying text to clipboard:", error);
    });
  }; 

  return(
  <Modal show={showModal} onHide={handleClose}>
    <Modal.Header closeButton>
      <Modal.Title>Share Workspace Link</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <div>{"http://localhost:3000/workspace/" + workspaceName}</div>
    </Modal.Body>
    <Modal.Footer className="d-flex justify-content-center">
      <Button
        variant="primary"
        onClick={() =>
          handleCopyClick("http://localhost:3000/workspace/" + workspaceName)
        }
      >
        Copy Link to Clipboard
      </Button>
    </Modal.Footer>
  </Modal>);
}
