import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import QuestionForm from "./QuestionForm";

const QuestionSettings = () => {
  const { project_name } = useParams();
  const fakeData = [
    { question: "What are the primary location(s) in this source?", id: 0 },
    {
      question: "What are the primary time(s) and date(s) in this source?",
      id: 1,
    },
    { question: "Who are the primary actor(s) in this source?", id: 2 },
    { question: "General Summary of Source:", id: 3 },
  ];

  return (
    <div>
      <div style={{ paddingTop: "2%", width: "75%", margin: "auto" }}>
        <h2 style={{ paddingTop: "1%", fontWeight: "bold " }}>
          Project {project_name} Question Form{" "}
        </h2>
        {fakeData.map((item) => (
          <div style={{ paddingTop: "1%" }} key={item.id}>
            {/* Create elements based on item properties */}
            <QuestionForm source={item}></QuestionForm>
          </div>
        ))}
      </div>
      <div style={{ margin: "auto", textAlign: "center" }}>
        <Button type="submit" className="btn btn-lg">
          Submit All
        </Button>
      </div>
    </div>
  );
};

export default QuestionSettings;
