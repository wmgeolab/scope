import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import { Row, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

export default function WorkspaceModal(props) {
  const { showModal, handleExitCreateModal, triggerCreation, error, errorMes } =
    props;

  const [tempErrorState, setTempErrorState] = useState(false);
  const [tempWorkspaceName, setTempWorkspaceName] = useState("");
  const [tempWorkspacePassword, setTempWorkspacePassword] = useState("");
  // errorState,
  // handleCloseCreate,

  const handleAttemptCreate = () => {
    if (tempWorkspaceName === "" || tempWorkspacePassword === "") {
      setTempErrorState(true);
    } else {
      setTempErrorState(false);
      triggerCreation(tempWorkspaceName, tempWorkspacePassword);
      if (!error) handleExitCreateModal();
      setTempWorkspaceName("");
      setTempWorkspacePassword("");
    }
  };

  return (
    <Modal show={showModal} onHide={handleExitCreateModal}>
      <Modal.Header closeButton>
        <Modal.Title> Create New Workspace</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form.Control
          type="email"
          placeholder="* Enter Workspace Name"
          onChange={(name) => setTempWorkspaceName(name.target.value)}
        />
        <Form.Control
          type="email"
          placeholder="* Enter Password"
          onChange={(name) => setTempWorkspacePassword(name.target.value)}
        />
        <Row>
          {tempErrorState ? (
            <Row className="d-flex justify-content-center text-danger">
              ** Please fill in all of the required answers. **
            </Row>
          ) : null}
          {errorMes ? (
            <Row className="d-flex justify-content-center text-danger">
              {errorMes}
            </Row>
          ) : null}
        </Row>
      </Modal.Body>
      <Modal.Footer className="d-flex justify-content-center">
        <Button variant="primary" onClick={handleAttemptCreate}>
          Create Workspace
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
