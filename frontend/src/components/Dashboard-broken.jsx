import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Queries from "./Queries";
import Results from "./Results";
import "../assets/css/main.css";
import LoginGithub from "react-login-github";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";

//import axios from "axios";

const Dashboard = () => {
  const onFailure = (response) => console.error(response);

  // https://www.freecodecamp.org/news/how-to-persist-a-logged-in-user-in-react/
  // const [username, setUsername] = useState("");
  // const [password, setPassword] = useState("");
  const [user, setUser] = useState();
  const [login, setLogin] = useState(false);
  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  }));

  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    console.log(loggedInUser);
    if (loggedInUser) {
      // const foundUser = JSON.parse(loggedInUser);
      setLogin(true);
      setUser(loggedInUser);
    }
  }, []);

  const handleSubmit = async (e) => {
    console.log(e.code);
    let token = await fetch("http://127.0.0.1:8000/dj-rest-auth/github", {
      method: "POST",
      headers: {
        // "Content-Type": "application/x-www-form-urlencoded",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: e.code }),
    });

    token.json().then((res) => {
      console.log(res);
      localStorage.setItem("user", res.key); //store the user in local storage
      setLogin(true);
    });
  };

  const handleLogout = () => {
    localStorage.clear();
    setLogin(false);
  };

  return (
    // <div>
    //   <div id="page-wrapper">
    //     {/* <!-- Header --> */}
    //     <section id="header" className="wrapper">
    //       <Grid container spacing={2}>
    //         <Grid item xs={4}></Grid>
    //         <Grid item xs={4}>
    //           <nav id="nav">
    //             <ul>
    //               <li className="current">
    //                 <a href="/">Dashboard</a>
    //               </li>
    //               <li>
    //                 <a href="/queries">Queries</a>
    //               </li>
    //             </ul>
    //           </nav>
    //         </Grid>
    //         <Grid item xs={4}>
    //           {login ? (
    //             // <div style={{ paddingLeft: 100 }}>
    //             <button
    //               onClick={handleLogout}
    //               style={{ float: "right", marginRight: "2em" }}
    //             >
    //               Logout
    //             </button>
    //           ) : (
    //             // </div>
    //             <LoginGithub //github gives back code give to backend, backend has client id and client secret (never transmit the secret)
    //               className="button style1 large"
    //               clientId="75729dd8f6e08419c896"
    //               onSuccess={handleSubmit}
    //               onFailure={onFailure}
    //             />
    //           )}
    //         </Grid>
    //       </Grid>
    //     </section>
    //   </div>
    // </div>
    <div>
      <div id="page-wrapper">
        {/* <!-- Header --> */}

        <section id="header" className="wrapper">
          {/* </Box> */}

          {/* <!-- Logo --> */}
          <div id="logo" style={{ margin: -100 }}>
            <h1>
              <a>SCOPE</a>
            </h1>
            <p>A free responsive site template by HTML5 UP</p>
          </div>
          <div
            style={{
              display: "flex",
              marginLeft: "auto",
              paddingLeft: 650,
            }}
          >
            <nav id="nav">
              <ul style={{ justifyContent: "space-around" }}>
                <li className="current">
                  <a href="/">Dashboard</a>
                </li>
                <li>
                  <a href="/queries">Queries</a>
                </li>
              </ul>
              {/* <Box sx={{ height: 400, width: "100%" }}> */}
              {login ? (
                // <div style={{ paddingLeft: 100 }}>
                <button
                  onClick={handleLogout}
                  style={{ float: "right", marginRight: "2em" }}
                >
                  Logout
                </button>
              ) : (
                // </div>
                <LoginGithub //github gives back code give to backend, backend has client id and client secret (never transmit the secret)
                  className="button style1 large"
                  clientId="75729dd8f6e08419c896"
                  onSuccess={handleSubmit}
                  onFailure={onFailure}
                />
              )}
            </nav>
          </div>
          {/* <!-- Nav --> */}
        </section>

        {/* <!-- Intro --> */}
        <section id="intro" className="wrapper style1">
          <div className="title">About</div>
          <div className="container">
            {/* <p className="style1">
              So in case you were wondering what this is all about ...
            </p> */}
            <p className="style2">
              Escape Velocity is a free responsive
              <br className="mobile-hide" />
              site template by{" "}
              <a href="http://html5up.net" className="nobr">
                HTML5 UP
              </a>
            </p>
            <p className="style3">
              It's <strong>responsive</strong>, built on <strong>HTML5</strong>{" "}
              and <strong>CSS3</strong>, and released for free under the{" "}
              <a href="http://html5up.net/license">
                Creative Commons Attribution 3.0 license
              </a>
              , so use it for any of your personal or commercial projects
              &ndash; just be sure to credit us!
            </p>
          </div>
        </section>
      </div>

      {/* <!-- Scripts --> */}
      {/* <script src="assets/js/jquery.min.js"></script>
      <script src="assets/js/jquery.dropotron.min.js"></script>
      <script src="assets/js/browser.min.js"></script>
      <script src="assets/js/breakpoints.min.js"></script>
      <script src="assets/js/util.js"></script>
      <script src="assets/js/main.js"></script> */}
    </div>
  );
};

export default Dashboard;
