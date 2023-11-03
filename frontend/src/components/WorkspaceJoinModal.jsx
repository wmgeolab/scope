import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";
import { Button } from "react-bootstrap";

export default function WorkspaceJoinModal(props) {
  const {
    showModal,
    setWorkspaceName,
    setWorkspacePassword,
    handleExitJoinModal,
    setTriggerJoinApiCall,
  } = props;

  const [tempErrorState, setTempErrorState] = useState(false);
  const [tempWorkspaceName, setTempWorkspaceName] = useState("");
  const [tempWorkspacePassword, setTempWorkspacePassword] = useState("");
  // errorState,
  // handleCloseCreate,

  // To ask Lena about:
    // Is there a way to grab a user's name?
    // Will be necessary for API calls and filtering.
    
  const handleAttemptCreate = () => {
    if (tempWorkspaceName === "" || tempWorkspacePassword === "") {
      setTempErrorState(true);
    } else {
      setTempErrorState(false);
      setWorkspaceName(tempWorkspaceName);
      setWorkspacePassword(tempWorkspacePassword);
      setTriggerJoinApiCall(true);
      handleExitJoinModal();
      setTempWorkspaceName('');
      setTempWorkspacePassword('');
    }
  };
  
  return (
    <Modal show={showModal} onHide={handleExitJoinModal}>
      <Modal.Header closeButton onClick={handleExitJoinModal}>
        <Modal.Title> Join Existing Workspace</Modal.Title>
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
            <Row className="d-flex justify-content-center text-danger" >
            ** Please fill in all of the required answers. **
            </Row>
          ) : null}
        </Row>
      </Modal.Body>
      <Modal.Footer className="d-flex justify-content-center">
        <Button variant="primary" onClick={handleAttemptCreate}>
          Join Workspace
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
