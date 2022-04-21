import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Queries from "./Queries";
import Results from "./Results";
import "../assets/css/main.css";
import LoginGithub from "react-login-github";
//import axios from "axios";

const Dashboard = () => {
  const onFailure = (response) => console.error(response);

  // https://www.freecodecamp.org/news/how-to-persist-a-logged-in-user-in-react/
  // const [username, setUsername] = useState("");
  // const [password, setPassword] = useState("");
  const [user, setUser] = useState();
  const [login, setLogin] = useState(false);

  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    console.log(loggedInUser);
    if (loggedInUser) {
      // const foundUser = JSON.parse(loggedInUser);
      setLogin(true); //need to figure out where to place this so it will change states, but the changes persist across refresh (store in local storage along with user?)
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
    <div>
      <div id="page-wrapper">
        <div>
          {login ? (
            <button onClick={handleLogout}>Logout</button>
          ) : (
            <LoginGithub //github gives back code give to backend, backend has client id and client secret (never transmit the secret)
              className="button style1 large"
              clientId="75729dd8f6e08419c896"
              onSuccess={handleSubmit}
              onFailure={onFailure}
            />
          )}
        </div>

        {/* <!-- Header --> */}
        <section id="header" className="wrapper">
          {/* <!-- Logo --> */}
          <div id="logo">
            <h1>
              <a>SCOPE</a>
            </h1>
            <p>A free responsive site template by HTML5 UP</p>
          </div>

          {/* <!-- Nav --> */}
          <nav id="nav">
            <ul>
              {/* <li><a href="left-sidebar.html">Left Sidebar</a></li> */}
              {/* <li><a href="right-sidebar.html">Right Sidebar</a></li> */}
              {/* <li><a href="no-sidebar.html">No Sidebar</a></li> */}
              <li className="current">
                <a href="/">Dashboard</a>
              </li>
              <li>
                <a href="/queries">Queries</a>
              </li>
              <li>
                <a href="/results">Results</a>
              </li>
              {/* <li>
                <a href="/login">Login</a>
              </li> */}
            </ul>
          </nav>
        </section>
        {/* <!-- Intro --> */}
        <section id="intro" className="wrapper style1">
          <div className="title">The Introduction</div>
          <div className="container">
            <p className="style1">
              So in case you were wondering what this is all about ...
            </p>
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
            <ul className="actions">
              <li>
                <a href="#" className="button style3 large">
                  Proceed
                </a>
              </li>
            </ul>
          </div>
        </section>
        <section id="footer" className="wrapper">
          <div className="title">The Rest Of It</div>
          <div className="container">
            <header className="style1">
              <h2>Ipsum sapien elementum portitor?</h2>
              <p>
                Sed turpis tortor, tincidunt sed ornare in metus porttitor
                mollis nunc in aliquet.
                <br />
                Nam pharetra laoreet imperdiet volutpat etiam feugiat.
              </p>
            </header>
            <div className="row">
              <div className="col-6 col-12-medium">
                {/* <!-- Contact Form --> */}
                <section>
                  <form method="post" action="#">
                    <div className="row gtr-50">
                      <div className="col-6 col-12-small">
                        <input
                          type="text"
                          name="name"
                          id="contact-name"
                          placeholder="Name"
                        />
                      </div>
                      <div className="col-6 col-12-small">
                        <input
                          type="text"
                          name="email"
                          id="contact-email"
                          placeholder="Email"
                        />
                      </div>
                      <div className="col-12">
                        <textarea
                          name="message"
                          id="contact-message"
                          placeholder="Message"
                          rows="4"
                        ></textarea>
                      </div>
                      <div className="col-12">
                        <ul className="actions">
                          <li>
                            <input
                              type="submit"
                              className="style1"
                              value="Send"
                            />
                          </li>
                          <li>
                            <input
                              type="reset"
                              className="style2"
                              value="Reset"
                            />
                          </li>
                        </ul>
                      </div>
                    </div>
                  </form>
                </section>
              </div>
              <div className="col-6 col-12-medium">
                {/* <!-- Contact --> */}
                <section className="feature-list small">
                  <div className="row">
                    <div className="col-6 col-12-small">
                      <section>
                        <h3 className="icon solid fa-home">Mailing Address</h3>
                        <p>
                          Untitled Corp
                          <br />
                          1234 Somewhere Rd
                          <br />
                          Nashville, TN 00000
                        </p>
                      </section>
                    </div>
                    <div className="col-6 col-12-small">
                      <section>
                        <h3 className="icon solid fa-comment">Social</h3>
                        <p>
                          <a href="#">@untitled-corp</a>
                          <br />
                          <a href="#">linkedin.com/untitled</a>
                          <br />
                          <a href="#">facebook.com/untitled</a>
                        </p>
                      </section>
                    </div>
                    <div className="col-6 col-12-small">
                      <section>
                        <h3 className="icon solid fa-envelope">Email</h3>
                        <p>
                          <a href="#">info@untitled.tld</a>
                        </p>
                      </section>
                    </div>
                    <div className="col-6 col-12-small">
                      <section>
                        <h3 className="icon solid fa-phone">Phone</h3>
                        <p>(000) 555-0000</p>
                      </section>
                    </div>
                  </div>
                </section>
              </div>
            </div>
            <div id="copyright">
              <ul>
                <li>&copy; Untitled.</li>
                <li>
                  Design: <a href="http://html5up.net">HTML5 UP</a>
                </li>
              </ul>
            </div>
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
