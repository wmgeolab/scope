import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert } from "@mui/material/";

const Workspaces = () => {
      
  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      <div>
        <h1>401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
        your access, please return to the <a href="/">dashboard</a> to log in
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
    // alert("Please log in")
  } else {
    return (
      <div></div>
    );
  }
};

export default Workspaces;
