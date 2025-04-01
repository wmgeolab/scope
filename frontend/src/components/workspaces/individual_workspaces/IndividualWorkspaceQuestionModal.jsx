import React, {useState, useEffect} from "react";
import { Modal } from "react-bootstrap";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import { API } from "../../../api/api";

export default function IndividualWorkspaceQuestionModal(props) {
    const { workspaceQuestions, showModal, handleClose, workspace_id } = props;

    console.log(workspaceQuestions);
    //console.log(workspaceResponses);

    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState([
      {id: workspaceQuestions[0]?.id, question: workspaceQuestions[0]?.question},
      {id: workspaceQuestions[1]?.id, question: workspaceQuestions[1]?.question},
      {id: workspaceQuestions[2]?.id, question: workspaceQuestions[2]?.question},
      {id: workspaceQuestions[3]?.id, question: workspaceQuestions[3]?.question}
    ]);

    console.log("Upon initialization, formData is: ", formData);
    //console.log(workspaceResponses[0].source_id)

 

    const handleInputChange = (idx, field, value) => {
      const updatedFormData = [...formData];
      updatedFormData[idx][field] = value;
      setFormData(updatedFormData);
      console.log(formData)
    };

    const handleSubmit = async () => {
      setLoading(true)
      // Call backend route to save edited question and response data
      console.log("Before calling POST route, formData array is:");
      console.log(formData);
      for (let i = 0; i < formData.length; i++) {
        // only call the route if the question actually contains anything
        if(formData[i].question) {
          let data = {
            id: formData[i].id,
            workspace_id: workspace_id,
            question: formData[i].question,
          };
  
          console.log(JSON.stringify(data), "in workspace question form");
          const response = await fetch(API.url(`/api/questions/?${workspace_id}`), {
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

        // only call ai response route if response contains something
        // if(formData[i].response) {
        //   let data = {
        //     source_id: workspaceResponses[0].source_id, // Using source_id
        //     summary: formData[3].response,
        //     entities: formData[2].response,
        //     locations: formData[0].response,
        //     workspace_id: workspace_id
        //   };

        //   console.log(JSON.stringify(data), "in workspace response form");
        //   const response = await fetch(API.url(`/api/ai_responses/${workspaceResponses[0].id}/`),  {
        //     method: "PUT",
        //     headers: {
        //         "Content-Type": "application/json",
        //         Authorization: "Token " + localStorage.getItem("user"),
        //     },
        //     body: JSON.stringify(data)
        // });
  
        //   const response_text = await response.json();
        //   console.log("Q Response update response: ", response_text);
        // }
      }

      await handleClose();
      
      setLoading(false);
        
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
        {/* <Form.Control 
          as="textarea" 
          rows={3} 
          //placeholder={workspaceResponses[0].locations}
          //value={formData[0].response}
          onChange={(e) => handleInputChange(0, 'response', e.target.value)}
        /> */}
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
        {/* <Form.Control 
          as="textarea" 
          rows={3} 
          //placeholder={workspaceResponses[0].entities}
          //value={formData[1].response}
          onChange={(e) => handleInputChange(1, 'response', e.target.value)}
        /> */}
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
        {/* <Form.Control 
          as="textarea" 
          rows={3} 
          //placeholder={workspaceResponses[0].entities}
          //value={formData[2].response}
          onChange={(e) => handleInputChange(2, 'response', e.target.value)}
        /> */}
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
        {/* <Form.Control 
          as="textarea" 
          rows={3} 
          //placeholder={workspaceResponses[0].summary}
          //value={formData[3].response}
          onChange={(e) => handleInputChange(3, 'response', e.target.value)}
        /> */}
        <Form.Text className="text-muted">
          Enter any questions related to the summarizing the article.
        </Form.Text>
      </Form.Group>
          
    </Modal.Body>
    <Modal.Footer className="d-flex justify-content-center">
      <Button variant="primary" onClick={handleSubmit} disabled={loading}>
        Apply To Workspace
      </Button>
    </Modal.Footer>
  </Modal>);
}