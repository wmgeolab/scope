import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import RefreshIcon from "@mui/icons-material/Refresh";

export default function QuestionModal(props) {
  const { showModal, handleGenerateBtnClick, handleCloseModal, sourceId } =
    props;
  const [locationDisabled, setLocationDisabled] = useState(true);
  const [timeDisabled, setTimeDisabled] = useState(true);
  const [actorDisabled, setActorDisabled] = useState(true);
  const [summaryDisabled, setSummaryDisabled] = useState(true);

  function resetAndCloseModal() {
    setLocationDisabled(true);
    setTimeDisabled(true);
    setActorDisabled(true);
    setSummaryDisabled(true);
    handleCloseModal();
  }
  return (
    <Modal show={showModal} onHide={resetAndCloseModal}>
      <Modal.Header closeButton onClick={resetAndCloseModal}>
        <Modal.Title> AI Form for Source: {sourceId} </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="textInput">
            <Row>
              <Col sm={9}>
                <Form.Label>
                  What are the primary location(s) in this source?
                  <Form.Check
                    type="switch"
                    id="location-switch"
                    label="Edit this section?"
                    onChange={() => setLocationDisabled(!locationDisabled)}
                  />
                </Form.Label>
              </Col>
              <Col sm={3}>
                <Button
                  onClick={() => handleGenerateBtnClick(sourceId)}
                  variant="secondary"
                  className="btn-sm"
                >
                  <RefreshIcon />
                  Generate
                </Button>
              </Col>
            </Row>
            <Form.Control
              type="text"
              placeholder="Pretend this is AI text..."
              disabled={locationDisabled}
            />
            <Form.Label>
              What are the primary time(s) and date(s) in this source?
              <Form.Check
                type="switch"
                id="time-switch"
                label="Edit this section?"
                onChange={() => setTimeDisabled(!timeDisabled)}
              />
            </Form.Label>
            <Form.Control
              type="text"
              placeholder="Pretend this is AI text.."
              disabled={timeDisabled}
            />
            <Form.Label>
              Who are the primary actor(s) in this source?
              <Form.Check
                type="switch"
                id="actor-switch"
                label="Edit this section?"
                onChange={() => setActorDisabled(!actorDisabled)}
              />
            </Form.Label>
            <Form.Control
              type="text"
              placeholder="Pretend this is AI text.."
              disabled={actorDisabled}
            />
            <Form.Label>
              General Summary of Source:
              <Form.Check
                type="switch"
                id="summary-switch"
                label="Edit this section?"
                onChange={() => setSummaryDisabled(!summaryDisabled)}
              />
            </Form.Label>
            <Form.Control
              type="text"
              placeholder="Pretend this is AI text.."
              disabled={summaryDisabled}
            />
            <div className="text-center mt-4">
              {(!summaryDisabled ||
                !locationDisabled ||
                !actorDisabled ||
                !summaryDisabled) && <Button onClick={resetAndCloseModal}> Save your changes</Button>}
            </div>
          </Form.Group>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
