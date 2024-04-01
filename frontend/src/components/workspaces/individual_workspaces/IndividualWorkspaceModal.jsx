import React, { useState, useEffect } from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

export default function IndividualWorkspaceModal(props) {
  /**
   * showModal => whether to display or not
   * handleClose => closes modal from parent
   * workspace_name => workspace name
   */
  const { showModal, 
          handleClose, 
          workspace_name } = props;

  // Copies the link to clipboard and closes modal
  const handleCopyClick = (params) => {
    navigator.clipboard.writeText(params);
    handleClose();
  };  

  return (
  <Modal show={showModal} onHide={handleClose}>
    <Modal.Header closeButton>
      <Modal.Title>Share Workspace Link</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <div>{"http://localhost:3000/workspace/" + workspace_name}</div>
    </Modal.Body>
    <Modal.Footer className="d-flex justify-content-center">
      <Button
        variant="primary"
        onClick={() =>
          handleCopyClick("http://localhost:3000/workspace/" + workspace_name)
        }
      >
        Copy Link to Clipboard
      </Button>
    </Modal.Footer>
  </Modal>);
}
