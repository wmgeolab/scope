import React, { useState } from "react";
import { Form } from 'react-bootstrap';
import Spinner from 'react-bootstrap/Spinner';

const QuestionForm = ({source}) => {

const [disabled, setDisabled] = useState(false);
const [AItext, setAItext] = useState("AI");
const [text, setText] = useState("");

const loading = () => {
    setDisabled(true);
    setTimeout(finished, 2000);
}

const finished = () => {
    setDisabled(false);
    setAItext("Regenerate");
    setText("<AI generated text>");
}

return (
        <Form>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
            <div>
                
            </div>
            <h3 style={{"display":"inline-block"}}>
                Question {source.id} : {source.question}
                
            </h3>
            
            <div style={{float:"right"}}>
                <input type="radio" class="btn-check"name={`options-outlined-${source.id}`} id={`danger-outlined-${source.id}`}  autocomplete="off" defaultChecked onClick={() => setDisabled(false)} disabled={disabled}/>
                <label class="btn btn-outline-primary" for={`danger-outlined-${source.id}`}> Manual</label>
                <input type="radio" class="btn-check"  name={`options-outlined-${source.id}`} id={`success-outlined-${source.id}`}   autocomplete="off"  onClick={() => loading()}/>
                <label class="btn btn-outline-primary" for={`success-outlined-${source.id}`}>{AItext} {'   '}
                    <Spinner
                        as="span"
                        animation="border"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                        hidden={!disabled}
                    />
                </label>
            </div>
<<<<<<< Updated upstream

            

=======
>>>>>>> Stashed changes
            <Form.Control as="textarea" disabled={disabled} value={text} onChange={(e) => setText(e.target.value)}/>
            </Form.Group>
        </Form>
    );

    }

export default QuestionForm;