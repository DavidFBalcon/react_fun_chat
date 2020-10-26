import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';
import App from './app';
import { Socket } from './Socket';
import './loginstyle.css';

export default function Login() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [pfp, setPfp] = useState('');

  function loginUser(response) {
    const name = response.getBasicProfile().getName();
    const email = response.getBasicProfile().getEmail();
    const pfp_url = `<img src="${response.getBasicProfile().getImageUrl()}">`;
    setPfp(pfp_url);
    const { id_token } = response.getAuthResponse();
    console.log(`Sending auth token ${id_token}`);
    Socket.emit('new google user', { name, email, idtoken: id_token });
  }

  function loginUserFail(response) {
    console.log('Unable to verify.');
  }

  function verifiedSession() {
    React.useEffect(() => {
      Socket.on('Verified', (data) => {
        console.log('Session verified, rerouting...');
        setLoggedIn(true);
        setUsername(data);
      });
    });
  }

  verifiedSession();

  if (loggedIn) {
    return (<App username={username} pfpTag={pfp} />);
  }

  return (
    <div className="outermost">
      <div className="inner">
        <h1 className="header">Really Awesome Chat App</h1>
        <GoogleLogin
          clientId="698177391473-sfucar7t4qoum5rpt14mso7vkbuh1lao.apps.googleusercontent.com"
          buttonText="Login"
          onSuccess={loginUser}
          onFailure={loginUserFail}
          cookiePolicy="single_host_origin"
        />
      </div>
    </div>
  );
}
