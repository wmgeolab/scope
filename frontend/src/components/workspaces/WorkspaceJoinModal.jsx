import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

export default function WorkspaceJoinModal(props) {
  /**
   * showModal  => the state variable on whether to render the modal or not
   * handleExitJoinModal => closes the modal and sets showModal to false on parent
   * triggerJoin => API request function to join
   * errorMes => Error message API func sets if there is a problem
   */
  const {
    showModal,
    handleExitJoinModal,
    triggerJoin,
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
  const handleAttemptJoin = () => {
    const workspace_name = document.getElementById("workspace_name").value;
    const workspace_password =
      document.getElementById("workspace_password").value;

    if (workspace_name === "" || workspace_password === "") {
      setTempErrorState(true);
    } else {
      setTempErrorState(false);
      triggerJoin(workspace_name, workspace_password).then((response) => {
        // If response is true, that means it was successful.
        if (response) {
          handleExitJoinModal();
          setSuccess(true);
          gatherWorkspaces();
          getTags();
        }
      });
    }
  };

  return (
    <div>
      <Modal show={showModal} onHide={handleExitJoinModal}>
        <Modal.Header closeButton onClick={handleExitJoinModal}>
          <Modal.Title> Join Existing Workspace</Modal.Title>
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
          <Button variant="primary" onClick={handleAttemptJoin}>
            Join Workspace
          </Button>
        </Modal.Footer>
      </Modal>

      <Snackbar
        open={success}
        autoHideDuration={6000}
        onClose={() => setSuccess(true)}
      >
        <Alert
          onClose={() => setSuccess(false)}
          severity="success"
          variant="filled"
          sx={{ width: "100%" }}
        >
          You've successfully join the workspace!
        </Alert>
      </Snackbar>
    </div>
  );
}
