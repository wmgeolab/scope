import React from "react";
import Form from "react-bootstrap/Form";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

export default function SendToWorkspaceModal(props) {
  const {
    showModal,
    handleClose,
    workspaceData,
    setSelectedWorkspace,
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
