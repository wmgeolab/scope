import React, { useState } from "react";
import { Form, FormGroup, FormCheck } from 'react-bootstrap';

const QuestionForm = ({source}) => {

return (
    
        <Form>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
            <div>
                
            </div>
            <h3 style={{"display":"inline-block"}}>
                Question {source.id} : {source.question}
                
            </h3>
            
            <div style={{float:"right"}}>
                <input type="radio" class="btn-check"  name={`options-outlined-${source.id}`} id={`success-outlined-${source.id}`}   autocomplete="off" checked/>
                <label class="btn btn-outline-primary" for={`success-outlined-${source.id}`}>AI</label>
                <input type="radio" class="btn-check"name={`options-outlined-${source.id}`} id={`danger-outlined-${source.id}`}  autocomplete="off"/>
                <label class="btn btn-outline-primary" for={`danger-outlined-${source.id}`}> Manual</label>
            </div>

            <Form.Control as="textarea" />
            </Form.Group>

        </Form>
        
)   ;

}

export default QuestionForm;