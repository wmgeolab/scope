import React from "react";
import { Link } from "react-router-dom";
import Queries from "./Queries";
import Results from "./Results";


const Dashboard = () => {
  return (
    <div>
      {/* <Navigation /> */}
      
				<h1>Dashboard </h1>
				 <Link to='/queries'>Go to Queries</Link> 
         <br></br> 
         <Link to='/results'>Go to Results</Link>
        
    </div>
  );
};
  
export default Dashboard;