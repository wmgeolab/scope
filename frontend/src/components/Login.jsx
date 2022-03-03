import React from 'react';
import ReactDOM from 'react-dom';
import LoginGithub from 'react-login-github';

import Dashboard from "./Dashboard";

function Login() {
    // const onSuccess = response => console.log(response);
    const onSuccess = response => {ReactDOM.render(<Dashboard />, document.getElementById('root'))}; {
        
    }
    const onFailure = response => console.error(response);

    return (
        <LoginGithub clientId="75729dd8f6e08419c896"
         onSuccess={onSuccess}
        // onSuccess={ReactDOM.render(<Dashboard />, document.getElementById('root'))}
        
        onFailure={onFailure} />
    );
}

export default Login;