import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Dialog, DialogTitle } from '@mui/material';
import './Login.css';



const Login = () => {
  const [error, setError] = useState(false);
  const [missingField, setMissingField] = useState(false);
  const navigate = useNavigate();

  const loginUser = form => {
    const username = form.target.username.value;
    const password = form.target.password.value;
    const data = {
        username: username,
        password: password,
    };

    if (!username || !password) {
      setMissingField(true);
      return;
    }

    return fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
   .then(data => data.json()) 
   .then((responseJson) => {
    if (responseJson.message && (responseJson.message === "logins details do not exist" || responseJson.message === "incorrect password")) {
      setError(true);
    } else {
      setError(false);
      sessionStorage.setItem("token", responseJson.token);
      navigate('/home')
    }
   });
}



  const handleSubmit = async form => {
    form.preventDefault();
    await loginUser(
      form
    );

  }

return(
    <div class = "login-background">
    <div className="login-wrapper">
        <div className='login-h-1'>Login Below</div>
        <div className='login-para'>Don't have an account?  <Link to="/register">Sign up</Link></div>
                
            <form className="LoginForm" onSubmit={handleSubmit}>
                <label className='login-label'>
                <div class="iconuser"></div>
                <input className='login-input' placeholder = "Username" type="text" name="username" />
                </label>
                <label className='login-label'>
                <div class="iconpw"></div>
                <input className='login-input' placeholder = "Password" type="password" name="password" />
                </label>
                <div class = "text-center">
                <button className='login-button' type="submit">Submit</button>
                </div>
            </form>
        <Dialog open={error} onClose={() => setError(false)} fullWidth={false}>
        <DialogTitle>
          Either these login details do not exist, or you have entered an incorrect password for the corresponding username.
        </DialogTitle>
      </Dialog>
      <Dialog open={missingField} onClose={() => setMissingField(false)} fullWidth={false}>
        <DialogTitle>
          Both a username and password is required to login.
        </DialogTitle>
      </Dialog>
    </div>
    </div>
  )
}

export default Login;