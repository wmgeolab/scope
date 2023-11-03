import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";
import { Button } from "react-bootstrap";

export default function IndividualWorkspaceModal(props) {
  const { showModal, handleClose } = props;

  <Modal show={show} onHide={handleClose}>
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
  </Modal>;
}
