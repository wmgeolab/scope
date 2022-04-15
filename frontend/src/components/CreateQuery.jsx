import React from "react";
import { Link } from "react-router-dom";
import LoginGithub from "react-login-github";

const CreateQuery = () => {
  const onSuccess = (response) => {
    console.log(response); //url doesn't change,
    //  state.auth ? ReactDOM.render(<Dashboard />, document.getElementById('root')): <h1>Please login!</h1>};
    //{ReactDOM.render(<Dashboard />, document.getElementById('root'))};
    //need to check if the state is authenticated or not, need to set the state to authenticated at some point
    //need to figure out what to do with callback
  };
  const onFailure = (response) => console.error(response);

  function submitQuery(e) {
    e.preventDefault();
    // Create the Post Request with the parameters
    let queryName = document.getElementById("queryName").value;
    let queryDescription = document.getElementById("queryDescription").value;
    let primaryKeyword = document.getElementById("primaryKeyword").value;
    let secondaryKeywords = document.getElementById("secondaryKeywords").value;

    var data = {
      name: queryName,
      description: queryDescription,
      keywords: [primaryKeyword, secondaryKeywords],
    };

    fetch("http://127.0.0.1:8000/api/queries/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });
  }

  return (
    // <div>
    //   {/* <Navigation /> */}

    // 		<h1>Dashboard </h1>
    // 		 <Link to='/queries'>Go to Queries</Link>
    //      <br></br>
    //      <Link to='/results'>Go to Results</Link>

    // </div>

    <div>
      <div id="page-wrapper">
        {/* <GithubButton
            onClick={() => {

            }}
          /> */}

        {/* do we want all the pages to have the login/logout button? */}
        <LoginGithub //github gives back code give to backend, backend has client id and client secret (never transmit the secret)
          className="button style1 large"
          clientId="75729dd8f6e08419c896"
          onSuccess={onSuccess} //this is a callback
          // onSuccess={ReactDOM.render(<Dashboard />, document.getElementById('root'))}
          //maybe can do something like onSuccess = this.setState...
          onFailure={onFailure}
        />
        {/* <!-- Header --> */}
        <section id="header" className="wrapper">
          {/* <!-- Logo --> */}
          <div id="logo">
            <h1>
              <a>SCOPE</a>
            </h1>
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
              <li>
                <a href="/login">Login</a>
              </li>
            </ul>
          </nav>
        </section>

        {/* <!-- Highlights --> */}
        <section id="highlights" className="wrapper style3">
          <div className="title">Create Query</div>
          <div className="container">
            <div className="form-style-5">
              <form>
                <fieldset>
                  <legend> Query Info</legend>
                  <input
                    type="text"
                    id="queryName"
                    placeholder="Query Name *"
                  ></input>
                  <input
                    type="text"
                    id="queryDescription"
                    placeholder="Query Description *"
                  ></input>
                  <input
                    type="text"
                    id="primaryKeyword"
                    placeholder="Primary Keyword (Only 1) *"
                  ></input>
                  <input
                    type="text"
                    id="secondaryKeywords"
                    placeholder="Secondary Keywords *"
                  ></input>
                </fieldset>
                <ul className="actions special">
                  <li>
                    <a onClick={submitQuery} className="button style1 large">
                      Submit Query
                    </a>
                  </li>
                </ul>
              </form>
            </div>
          </div>
        </section>
      </div>

      {/* <!-- Scripts --> */}
      <script src="assets/js/jquery.min.js"></script>
      <script src="assets/js/jquery.dropotron.min.js"></script>
      <script src="assets/js/browser.min.js"></script>
      <script src="assets/js/breakpoints.min.js"></script>
      <script src="assets/js/util.js"></script>
      <script src="assets/js/main.js"></script>
    </div>
  );
};

export default CreateQuery;
