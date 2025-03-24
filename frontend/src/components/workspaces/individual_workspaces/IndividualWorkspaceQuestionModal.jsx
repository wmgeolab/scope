import React, {useState, useEffect} from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";

export default function IndividualWorkspaceQuestionModal(props) {
    const { workspaceQuestions, showModal, handleClose, workspace_id } = props;

    console.log(workspaceQuestions);

    // const [locQuestion, setLocQuestion] = useState('');
    // const [dtQuestion, setDtQuestion] = useState('');
    // const [edit2, setEdit2] = useState(false);
    // const [actorsQuestion, setActorsQuestion] = useState('');
    // const [edit3, setEdit3] = useState(false);
    // const [summaryQuestion, setSummaryQuestion] = useState('');
    // const [edit4, setEdit4] = useState(false);

    const [formData, setFormData] = useState([
      {id: workspaceQuestions[0]?.id, question: workspaceQuestions[0]?.question, response: ''},
      {id: workspaceQuestions[1]?.id, question: workspaceQuestions[1]?.question, response: ''},
      {id: workspaceQuestions[2]?.id, question: workspaceQuestions[2]?.question, response: ''},
      {id: workspaceQuestions[3]?.id, question: workspaceQuestions[3]?.question, response: ''}
    ]);

    console.log("Upon initialization, formData is: ", formData);

 

    const handleInputChange = (idx, field, value) => {
      const updatedFormData = [...formData];
      updatedFormData[idx][field] = value;
      setFormData(updatedFormData);
      console.log(formData)
    };

    const handleSubmit = async () => {
      // Call backend route to save edited question and response data
      console.log("Before calling POST route, formData array is:");
      console.log(formData);
      for (let i = 0; i < formData.length; i++) {
        // only call the route if the question actually contains anything
        if(formData[i].question) {
          let data = {
            id: formData[i].id,
            workspace: workspace_id,
            question: formData[i].question,
          };
  
          console.log(JSON.stringify(data), "in workspace question form");
          const response = await fetch(`http://127.0.0.1:8000/api/questions/?${workspace_id}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + localStorage.getItem("user"),
            },
            body: JSON.stringify(data),
          });
  
          const response_text = await response.json();
          console.log("Question update response: ", response_text);
          
        }
      }
        
    }

  return(
  <Modal show={showModal} onHide={handleClose}>
    <Modal.Header closeButton>
      <Modal.Title>Add Workspace Questions</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      {/* <Form.Control
            type="email"
            placeholder="* Enter Question"
          //   onChange={(name) => setTempWorkspaceName(name.target.value)}
      /> */}
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Location Question</Form.Label>
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder={workspaceQuestions[0] ? workspaceQuestions[0].question : 'No existing question'}
          value={formData[0].question}
          onChange={(e) => handleInputChange(0, 'question', e.target.value)} 
        />
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder="Existing LLM Response"
          value={formData[0].response}
          onChange={(e) => handleInputChange(0, 'response', e.target.value)}
        />
        <Form.Text className="text-muted">
          Enter any questions related to the location of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Date/Time Question</Form.Label>
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder={workspaceQuestions[1] ? workspaceQuestions[1].question : 'No existing question'}
          value={formData[1].question}
          onChange={(e) => handleInputChange(1, 'question', e.target.value)} 
        />
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder="Existing LLM Response"
          value={formData[1].response}
          onChange={(e) => handleInputChange(1, 'response', e.target.value)}
        />
        <Form.Text className="text-muted">
          Enter any questions related to the date/time of the article's content.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Actors Question</Form.Label>
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder={workspaceQuestions[2] ? workspaceQuestions[2].question : 'No existing question'}
          value={formData[2].question}
          onChange={(e) => handleInputChange(2, 'question', e.target.value)} 
        />
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder="Existing LLM Response"
          value={formData[2].response}
          onChange={(e) => handleInputChange(2, 'response', e.target.value)}
        />
        <Form.Text className="text-muted">
          Enter any questions related to the actors present in an article.
        </Form.Text>
      </Form.Group>
      <Form.Group className="mb-3" controlId="question">
        <Form.Label>Summary Question</Form.Label>
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder={workspaceQuestions[3] ? workspaceQuestions[3].question : 'No existing question'}
          value={formData[3].question}
          onChange={(e) => handleInputChange(3, 'question', e.target.value)} 
        />
        <Form.Control 
          as="textarea" 
          rows={3} 
          placeholder="Existing LLM Response"
          value={formData[3].response}
          onChange={(e) => handleInputChange(3, 'response', e.target.value)}
        />
        <Form.Text className="text-muted">
          Enter any questions related to the summarizing the article.
        </Form.Text>
      </Form.Group>
          
      {/* <Form.Control
            type="email"
            placeholder="* Enter Question"
          //   onChange={(name) => setTempWorkspacePassword(name.target.value)}
      /> */}
    </Modal.Body>
    <Modal.Footer className="d-flex justify-content-center">
      <Button variant="primary" onClick={handleSubmit}>
        Apply To Workspace
      </Button>
    </Modal.Footer>
  </Modal>);
}