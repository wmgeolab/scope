import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

export default function WorkspaceModal(props) {
  const {
    showModal,
    setWorkspaceName,
    setWorkspacePassword,
    handleCloseCreate,
    handleExitCreateModal,
    triggerCreation,
    error,
    errorMes,
  } = props;

  const [tempErrorState, setTempErrorState] = useState(false);
  const [tempWorkspaceName, setTempWorkspaceName] = useState("");
  const [tempWorkspacePassword, setTempWorkspacePassword] = useState("");
  const [success, setSuccess] = React.useState(false);

  const handleCloseSuccessSnackbar = () => {
    setSuccess(false);
  };

  // errorState,
  // handleCloseCreate,

  const handleAttemptCreate = () => {
    if (tempWorkspaceName === "" || tempWorkspacePassword === "") {
      setTempErrorState(true);
    } else {
      setTempErrorState(false);
      triggerCreation(tempWorkspaceName, tempWorkspacePassword);

      // console.log("error", error);
      if (!error) handleExitCreateModal();
      setTempWorkspaceName("");
      setTempWorkspacePassword("");

      handleExitCreateModal(); // will close the modal but isn't checking for errors
      // window.location.reload(false); // refresh the page so the user can see their workspace
      setSuccess(true);
    }
  };

  return (
    <div>
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
      <Snackbar
        open={success}
        autoHideDuration={6000}
        onClose={handleCloseSuccessSnackbar}
      >
        <Alert
          onClose={handleCloseSuccessSnackbar}
          severity="success"
          variant="filled"
          sx={{ width: "100%" }}
        >
          Workspace created!
        </Alert>
      </Snackbar>
    </div>
  );
}
