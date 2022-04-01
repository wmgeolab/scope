import React, { useState, useEffect } from "react";
import Link from 'react-dom';
import {BrowserRouter, Routes, Route, useNavigate, Navigate} from "react-router-dom";
import './App.css';
import LoginGithub from 'react-login-github';

import Login from "./components/Login"; //  can have code here or on different component
import Dashboard from "./components/Dashboard";
import Queries from "./components/Queries";
import Results from "./components/Results";

function App() {

  
  return (
    <BrowserRouter>
      {/* <Router> */}
      <div className="App">
      </div>

        <Routes>
          {/* this makes it so I can't go to any of the routes without logging in */}
           {/* <Route path="/dashboard" render={() => <Dashboard />}/>  */}
            {/* <Route element={<Login />}>    */}
             <Route exact path="/" element={<Dashboard />} /> 
            <Route exact path="/queries" element={<Queries />} />
            <Route exact path="/results" element={<Results />} />
         {/* </Route>  */}
        </Routes>
      {/* </Router> */}
    </BrowserRouter>
  );
}

// const Login = () => { //changed from function
//   let navigate = useNavigate();

//   const [state, setState] = useState({
//       auth: false
//     });


//   useEffect(() => {  //is a listener
//       if(state.auth){
//         console.log("Navigate to the dashboard isn't working here");
//      <Navigate path="/dashboard" element={<Dashboard />}/>
//       }
      

//   }, [state.auth]);
//   // const onSuccess = response => console.log(response);
//   const onSuccess = response => {
//       setState({ auth: true }); //url doesn't change, 
//     //  state.auth ? ReactDOM.render(<Dashboard />, document.getElementById('root')): <h1>Please login!</h1>};
//   //{ReactDOM.render(<Dashboard />, document.getElementById('root'))}; 
//       //need to check if the state is authenticated or not, need to set the state to authenticated at some point
//       //need to figure out what to do with callback
//   };
//   const onFailure = response => console.error(response); 

//   return (//have the div below to be able to add headers
//       <><div></div> 
    
//       <LoginGithub clientId="75729dd8f6e08419c896"
//           onSuccess={onSuccess} //this is a callback



//           // onSuccess={ReactDOM.render(<Dashboard />, document.getElementById('root'))}
//           //maybe can do something like onSuccess = this.setState...
//           onFailure={onFailure} />
          
//           </>

//       //need to set state again when user logs out -- need a logout button?
//       //look at examples I sent to Isabella with sign in and sign out button and different links
//       //maybe go through a tutorial to get that working
//       //state.auth ? <Outlet /> : <Navigate  to= "/" />;
//   );
// }

export default App;
