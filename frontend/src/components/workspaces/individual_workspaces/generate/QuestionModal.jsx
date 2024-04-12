import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import { Row, Col, Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";

export default function QuestionModal(props) {
  const { showModal, handleCloseModal, sourceId } = props;
  const [locationDisabled, setLocationDisabled] = useState(true);
  const [timeDisabled, setTimeDisabled] = useState(true);
  const [actorDisabled, setActorDisabled] = useState(true);
  const [summaryDisabled, setSummaryDisabled] = useState(true);

  return (
    <Modal show={showModal} onHide={handleCloseModal}>
      <Modal.Header closeButton onClick={handleCloseModal}>
        <Modal.Title> AI Form for Source: {sourceId} </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="textInput">
            <Form.Label>
              What are the primary location(s) in this source?
              <Form.Check
                type="switch"
                id="location-switch"
                label="Edit this section?"
                onChange={() => setLocationDisabled(!locationDisabled)}
               
              />
            </Form.Label>
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
              {(!summaryDisabled || !locationDisabled || !actorDisabled || !summaryDisabled) && (
                <Button> Save your changes</Button>
              )}
            </div>
          </Form.Group>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
