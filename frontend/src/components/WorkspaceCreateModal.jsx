import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";
import { Button } from "react-bootstrap";

export default function WorkspaceModal(props) {
  const {
    showModal,
    setWorkspaceName,
    setWorkspacePassword,
    handleCloseCreate,
    handleExitCreateModal,
    setTriggerCreateApiCall,
  } = props;

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
      setWorkspaceName(tempWorkspaceName);
      setWorkspacePassword(tempWorkspacePassword);
      setTriggerCreateApiCall(true);
      handleExitCreateModal();
      setTempWorkspaceName('');
      setTempWorkspacePassword('');
    }
  };

  return (
    <Modal show={showModal} onHide={handleExitCreateModal}>
      <Modal.Header closeButton onClick={handleCloseCreate}>
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
            <Row className="d-flex justify-content-center text-danger" >
            ** Please fill in all of the required answers. **
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
