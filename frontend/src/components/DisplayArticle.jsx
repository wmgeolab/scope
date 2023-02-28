import React from "react";

const DisplayArticle = () => {
  //   var { Readability } = require("@mozilla/readability");
  if (localStorage.getItem("user") === null) {
    // fix?
    return (
      <div>
        <h1>401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
        your access, please return to the <a href="/">dashboard</a> to log in
        {/*do we want a popup so user is never taken to queries*/}
      </div>
    );
  } else {
    return <div>hello</div>;
  }
};

export default DisplayArticle;
