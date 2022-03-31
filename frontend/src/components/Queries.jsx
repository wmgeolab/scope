import React from "react";
import { Link } from "react-router-dom";

const Queries = () => {
  return (
    <div>
      <head>
  		<title>SCOPE</title>
  		<meta charset="utf-8" />
  		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
      <link rel="stylesheet" href="assets/css/table.css" />
  		<link rel="stylesheet" href="assets/css/main.css" />

  	</head>
  	<body class="homepage is-preload">
  		<div id="page-wrapper">

  			{/* <!-- Header --> */}
  				<section id="header" class="wrapper">

  					{/* <!-- Logo --> */}
  						<div id="logo">
  							<h1><a>SCOPE</a></h1>
  						</div>

  					{/* <!-- Nav --> */}
  						<nav id="nav">
  							<ul>
  								{/* <li><a href="left-sidebar.html">Left Sidebar</a></li> */}
  								{/* <li><a href="right-sidebar.html">Right Sidebar</a></li> */}
  								{/* <li><a href="no-sidebar.html">No Sidebar</a></li> */}
  								<li><a href="/">Dashboard</a></li>
  								<li class="current"><a href='/queries'>Queries</a></li>
  								<li><a href='/results'>Results</a></li>
  								<li><a href='/login'>Login</a></li>
  							</ul>
  						</nav>

  				</section>



  			{/* <!-- Main --> */}
  				<section id="main" class="wrapper style2">
  					<div class="title">Queries</div>
            <table class="content-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Keywords</th>
                  <th>User</th>
                </tr>
              </thead>
              <tbody>
                <tr>

                  <td>1</td>
                  <td><a href="/">Russian hydroelectric activity in Africa</a></td>
                  <td>Russia, Water, Africa</td>
                  <td>michaelrfoster</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td><a href="/">Covid-19 impact on USA vs Russia</a></td>
                  <td>Covid, USA, Russia</td>
                  <td>LazyRiver18</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td><a href="/">Food shortages in Ukrane resulting from Russian invasion</a></td>
                  <td>Ukrane, Russia, Food, Shortages</td>
                  <td>istwu</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td><a href="/">Recent communication between China and Russia</a></td>
                  <td>China, Russia, Talks</td>
                  <td>devsaxena974</td>
                </tr>
              </tbody>
            </table>
  					<div class="container">



  						{/* <!-- Features --> */}
  							<section id="features">


  								<ul class="actions special">
  									<li><a href="#" class="button style1 large">Create New Query</a></li>
  								</ul>
  							</section>

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

  	</body>
    </div>
  );
};

export default Queries;