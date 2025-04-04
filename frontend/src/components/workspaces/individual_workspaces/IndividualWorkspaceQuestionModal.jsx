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
    const [newQuestion, setNewQuestion] = useState("");


    // If we only have one question
    // const [formData, setFormData] = useState({
    //   id: workspaceQuestions[0]?.id || null,
    //   question: workspaceQuestions[0]?.question || "",
    // });
    const [formData, setFormData] = useState([]);
    useEffect(() => {
      if (workspaceQuestions && workspaceQuestions.length > 0) {
        setFormData(workspaceQuestions);
      }
    }, [workspaceQuestions]);

    console.log("Upon initialization, formData is: ", formData);
    //console.log(workspaceResponses[0].source_id)

 

    // const handleInputChange = (idx, field, value) => {
    //   const updatedFormData = [...formData];
    //   updatedFormData[idx][field] = value;
    //   setFormData(updatedFormData);
    //   console.log(formData)
    // };

    const handleInputChange = (field, value) => {
      setFormData({ ...formData, [field]: value });
      console.log("Updated formData: ", formData);
    };

    const handleSubmit = async () => {
      setLoading(true)
      // Call backend route to save edited question and response data
      console.log("Before calling POST route, formData array is:");
      console.log(formData);
      // for (let i = 0; i < formData.length; i++) {
      //   // only call the route if the question actually contains anything
      //   if(formData[i].question) {
      //     let data = {
      //       id: formData[i].id,
      //       workspace_id: workspace_id,
      //       question: formData[i].question,
      //     };
  
      //     console.log(JSON.stringify(data), "in workspace question form");
      //     const response = await fetch(API.url(`/api/questions/?${workspace_id}`), {
      //       method: "POST",
      //       headers: {
      //         "Content-Type": "application/json",
      //         Authorization: "Token " + localStorage.getItem("user"),
      //       },
      //       body: JSON.stringify(data),
      //     });
  
      //     const response_text = await response.json();
      //     console.log("Question update response: ", response_text);
          
      //   }

      if (newQuestion.trim()) {
        let data = {
          id: formData.id,
          workspace_id: workspace_id,
          question: newQuestion,
        };
  
        console.log("Submitting data:", JSON.stringify(data));
  
        const response = await fetch(API.url(`/api/questions/?${workspace_id}`), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + localStorage.getItem("user"),
          },
          body: JSON.stringify(data),
        });
  
        const response_text = await response.json();
        console.log("Question update response:", response_text);

        await handleClose();
      
        // Add new question to list
        setFormData((prev) => [...prev, response_text]);
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
      

      setNewQuestion("");
      setLoading(false);
        
    }

    // Function to handle the deleting of previous questions
    const handleDelete = async (id) => {
      const confirmed = window.confirm("Are you sure you want to delete this question?");
      if (!confirmed) return;
  
      // const response = await fetch(API.url(`/api/questions/${id}/`), {
      //   method: "DELETE",
      //   headers: {
      //     "Content-Type": "application/json",
      //     Authorization: "Token " + localStorage.getItem("user"),
      //   },
      // });
      console.log("Question to be deleted: ", id);
  
      // if (response.ok) {
      //   setFormData((prev) => prev.filter((q) => q.id !== id));
      // }
    };

  return(
    <Modal show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Manage Workspace Question</Modal.Title>
      </Modal.Header>
      {/* <Modal.Body>
        <Form.Group className="mb-3" controlId="question">
          <Form.Label>Workspace Question</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder={formData.question || "Enter your question here"}
            value={formData.question}
            onChange={(e) => handleInputChange("question", e.target.value)}
          />
          <Form.Text className="text-muted">
            Enter or edit existing question.
          </Form.Text>
        </Form.Group>
      </Modal.Body> */}
      <Modal.Body>
        <Form.Group className="mb-3" controlId="newQuestion">
          <Form.Label>Add New Question</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder="Enter a new question..."
            value={newQuestion}
            onChange={(e) => setNewQuestion(e.target.value)}
          />
        </Form.Group>

        <div className="d-flex flex-column gap-2">
          {formData.map((q) => (
            <div
              key={q.id}
              style={{
                background: "linear-gradient(135deg, #c2e9fb 0%, #a1c4fd 100%)",
                borderRadius: "8px",
                padding: "10px 15px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <span style={{ flexGrow: 1 }}>{q.question}</span>
              <Button
                variant="danger"
                size="sm"
                className="ms-2"
                onClick={() => handleDelete(q.id)}
              >
                Delete
              </Button>
            </div>
          ))}
        </div>
      </Modal.Body>
      <Modal.Footer className="d-flex justify-content-center">
        <Button variant="primary" onClick={handleSubmit} disabled={loading}>
          Save Question
        </Button>
      </Modal.Footer>
    </Modal>);
  // 
}