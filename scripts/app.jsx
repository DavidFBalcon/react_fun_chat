import React, { useState, useRef } from 'react';
import ScrollToBottom from 'react-scroll-to-bottom';
import PropTypes from 'prop-types';
import ChatLog from './ChatLog';
import { Socket } from './Socket';
import './appstyle.css';

function App(props) {
  const [userMsg, setMsg] = useState([]);
  const [userCount, setCount] = useState(0);
  const userInput = useRef();
  // RETRIEVING THE CHAT HISTORY
  React.useEffect(() => { Socket.emit('retrieve history'); }, []);

  React.useEffect(() => {
    Socket.on('sent history', setMsg);
    return () => {
      Socket.off('sent history', setMsg);
    };
  }, []);

  // RETRIEVE USER COUNT DYNAMICALLY
  React.useEffect(() => { Socket.emit('user update'); }, []);

  React.useEffect(() => {
    Socket.on('user change', setCount); return () => {
      Socket.off('user change', setCount);
    };
  }, []);

  function sendMessageButton(e) {
    const addMsg = userInput.current.value;
    if (addMsg === '') return;
    Socket.emit('new message', { message: addMsg, user: props.username, pfp_url: props.pfpTag });
    userInput.current.value = null;
    e.preventDefault();
  }

  function sendMessageOnkey(e) {
    if (e.key === 'Enter') {
      sendMessageButton(e);
    }
  }

  function updateMsg(data) {
    setMsg((prevUserMsg) => [...prevUserMsg, {
      message: data.message, user: data.user, pfp_url: data.pfp_url,
    }]);
  }

  function getNewMessages() {
    React.useEffect(() => {
      Socket.on('message display', updateMsg);
      return () => {
        Socket.off('message display', updateMsg);
      };
    });
  }

  getNewMessages();

  return (
    <div className="outer">
      <div className="container">
        <div className="pageTitle">
          <h1>Chatroom</h1>
        </div>
        <div className="welcome">
          <h1>
            Welcome
            {' '}
            {props.username}
            !
          </h1>
          <h3>
            There are currently
            {' '}
            {userCount}
            {' '}
            users online.
          </h3>
        </div>
        <ScrollToBottom className="message_container">
          <ChatLog history={userMsg} reader={props.username} />
        </ScrollToBottom>
        <input ref={userInput} type="text" onKeyDown={sendMessageOnkey} />
        <button type="button" onClick={sendMessageButton}>Send Message</button>
      </div>
    </div>
  );
}

App.propTypes = {
  username: PropTypes.string.isRequired,
  pfpTag: PropTypes.string.isRequired,
};

export default App;
