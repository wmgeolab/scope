import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import { Container, Row, Col } from "react-bootstrap";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "./../images/pic10.jpg";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/questionsettings.css";
import NavBar from "./NavBar";
import QuestionForm from "./QuestionForm";

const QuestionSettings = () => {

    const fakeData = [
        {"question":"Lorem ipsum dolor sit amet?", "id":0},
        {"question":"consectetur adipiscing elit, sed do eiusmod tempor incididun?", "id":1},
        {"question":"Excepteur sint occaecat cupidatat non proident?", "id":2},
        {"question":"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris?", "id":3}
    ]

    return(
        <div>
        <NavBar></NavBar>
        <div style={{paddingTop:"2%", width:"75%", margin: "auto"}}>
            <h2 style={{ paddingTop: "1%", fontWeight: "bold " }}>Project [Name] Question Form </h2>
            {fakeData.map(item => (
                <div key={item.id}>
                {/* Create elements based on item properties */}
                <QuestionForm source={item}></QuestionForm>
                </div>
            ))}
        </div>
        <div style={{margin:"auto", textAlign:"center"}}>
        <Button type="submit" className="btn btn-lg">
                    Submit All
        </Button>
        </div>

        </div>
    )   
}

export default QuestionSettings;