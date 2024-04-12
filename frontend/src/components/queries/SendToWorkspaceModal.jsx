import React from "react";
import Form from "react-bootstrap/Form";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

/**
 * Model used to export sources within a query search into a workspace
 * Used in Results.jsx
 */
export default function SendToWorkspaceModal(props) {
  /**
   * showModal => Whether to show pop up or not
   * handleClose => Closes the model from parent
   * workspaceData => Contains the list of workspaces a user is part of 
   * selectedWorkspace => Holds the WS the user selects to send it to.
   * handleSend => Handles actually sending the workspaces.
   */
  const {
    showModal,
    handleClose,
    workspaceData,
    setSelectedWorkspace,
    setSelectedWorksapceName,
    selectedWorkspace,
    handleSend,
  } = props;

  return (
    <div>
      <Modal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Send to Workspace</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {/* You need to be part of a workspace to select one */}
          {workspaceData === undefined || workspaceData.length == 0 ? (
            <p>Please join or create a workspace first!</p>
          ) : (
            <p>Choose a Workspace:</p>
          )}
          <Form.Select
            aria-label="Default select example"
            value={selectedWorkspace}
            onChange={(e) => {
              console.log(e.target.value);
              console.log(e.target.value, "FULL TARGET");
              setSelectedWorkspace(e.target.value);
            }}
            disabled={workspaceData === undefined || workspaceData.length == 0}
          >
            {workspaceData.map((workspace, index) => (
              <option value={workspace.id}>{workspace.name}</option>
            ))}
          </Form.Select>
        </Modal.Body>
        <Modal.Footer>
          <Button
            onClick={handleSend}
            disabled={workspaceData === undefined || workspaceData.length == 0}
          >
            Send Selected to Workspace
          </Button>
          <Button variant="secondary" onClick={handleClose}>
            Cancel
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
