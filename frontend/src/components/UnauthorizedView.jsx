import React, { useState } from "react";

const UnauthorizedView = () => {
  return (
    <div>
      <h1>401 unauthorized</h1>Oops, looks like you've exceeded the SCOPE of
      your access, please return to the <a href="/">dashboard</a> to log in
    </div>
  );
};

export default UnauthorizedView;
