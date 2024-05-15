import React from "react";
import "./Register.css";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import validator from 'validator';
import { useNavigate } from "react-router-dom";
import "./Login/Login"

const Register = () => {
    const [usernameError, setUsernameError] = React.useState(false);
    const [emailError, setEmailError] = React.useState(false);
    const [passwordError, setPasswordError] = React.useState(false);
    const [passwordRegexError, setPasswordRegexError] = React.useState(false);

    const navigate = useNavigate();
  
    const handleSubmit = (event) => {
    event.preventDefault();

    let firstName = event.target.firstName.value;
    let lastName = event.target.lastName.value;
    let email = event.target.email.value;
    let username = event.target.username.value;
    let password1 = event.target.password1.value;
    let password2 = event.target.password2.value;
    
    if (validator.isStrongPassword(password1, {
      minLength: 8, minLowercase: 1, minUppercase: 1, minSymbols: 1
    })) {
      setPasswordRegexError(false);
    } else {
      setPasswordRegexError(true);
      return;
    }

    if (password2 !== password1) {
      setPasswordError(true);
      return;
    } else {
      setPasswordError(false);
    }
    register(firstName, lastName, username, email, password1);
};

  const register = (firstName, lastName, username, email, password) => {
    const data = {
      firstName: firstName,
      lastName: lastName,
      username: username,
      email: email,
      password: password,
    };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };

    fetch("http://localhost:5000/register", requestOptions)
        .then((response) => response.json())
        .then((responseJson) => {
        if (responseJson.code && responseJson.code != 200) {
          if (responseJson.message === 'username already exists')  {
            setUsernameError(true);
            setEmailError(false);
          } else {
            setEmailError(true);
            setUsernameError(false);
          }
        } else {
            sessionStorage.setItem("token", responseJson.token);
            navigate('/home')
        }
    });
};
  const getHelperText = () => {
    if (passwordRegexError) return "Must contain 8 characters, and at least 1 lower case, upper case, number and special character"
    if (passwordError) return "Does not match other password!";
  }

return (
    <div className = "login-background">
    <div className="register-display">
        <div className="regisiter-h-2">Create an Account</div>
        <form onSubmit={handleSubmit} className="register-form">
        <TextField name="firstName" type="text" required fullWidth label="First Name" sx={{backgroundColour: 'white'}} />
        <TextField name="lastName" type="text" required fullWidth label="Last Name" />
        <TextField name="username" error={usernameError} helperText={usernameError && "Username Taken!"} required fullWidth label="Username" />
        <TextField name="email" type="email" error={emailError} helperText={emailError && "Email Taken!"} inputProps={{ maxLength: 50 }} required fullWidth label="Email" />
        <TextField name="password1" type="password" inputProps={{ minLength: 6, maxLength: 30 }} required fullWidth label="Password" />
        <TextField
            name="password2"
            error={passwordError||passwordRegexError}
            helperText={getHelperText()}
            type="password"
            inputProps={{ minLength: 6 }}
            required
            fullWidth
            label="Confirm Password"
        />
        <Button variant="contained" color="primary" type="submit">
            Register
        </Button>
      </form>
    </div>
    </div>
  );
}

export default Register;