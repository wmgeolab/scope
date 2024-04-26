import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

export default function WorkspaceModal(props) {
  /**
   * showModal => the state variable on whether to render the modal or not
   * handleExitCreateModal => closes the modal and sets showModal to false on parent
   * triggerCreation => API request function to create
   * errorMes => Error message API func sets if there is a problem
   */
  const {
    showModal,
    handleExitCreateModal,
    triggerCreation,
    errorMes,
    gatherWorkspaces,
    getTags,
  } = props;

  // These are temporary validity state that don't deal with API validation
  // But only with user input validation : You need a name and a password!
  const [tempErrorState, setTempErrorState] = useState(false);
  // Whether to show a toast or not.
  const [success, setSuccess] = React.useState(false);

  /**
   * Triggers the API request and handles the UI from its response
   */
  const handleAttemptCreate = () => {
    const workspace_name = document.getElementById("workspace_name").value;
    const workspace_password =
      document.getElementById("workspace_password").value;

    if (workspace_name === "" || workspace_password === "") {
      setTempErrorState(true);
    } else {
      setTempErrorState(false);
      triggerCreation(workspace_name, workspace_password).then((response) => {
        // If response is true, successful creation.
        if (response) {
          handleExitCreateModal();
          setSuccess(true);
          gatherWorkspaces();
          getTags();
        }
      });
    }
  };

  return (
    <div>
      <Modal show={showModal} onHide={handleExitCreateModal}>
        <Modal.Header closeButton onClick={handleExitCreateModal}>
          <Modal.Title> Create New Workspace</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Control
            type="email"
            placeholder="* Enter Workspace Name"
            id="workspace_name"
          />
          <Form.Control
            type="email"
            placeholder="* Enter Password"
            id="workspace_password"
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
        onClose={() => setSuccess(false)}
      >
        <Alert
          onClose={() => setSuccess(false)}
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
