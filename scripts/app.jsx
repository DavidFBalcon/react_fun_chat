import React, { useState, useRef } from "react";
import ChatLog from "./ChatLog";
import { v4 } from "uuid";
import { Socket } from './Socket';
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'

export default function App(props) {
  const [userMsg, setMsg] = useState([]);
  const [userCount, setCount] = useState(0);
  const userInput = useRef();
  const currentUser = props.username;
  
  
  //RETRIEVING THE CHAT HISTORY
  React.useEffect(() => {
    Socket.emit('retrieve history')}, []);
  
  React.useEffect(() => {
    Socket.on('sent history', setMsg);
    return () => {
      Socket.off('sent history', setMsg);
      }
    }, []);
    
  //RETRIEVE USER COUNT DYNAMICALLY
  React.useEffect(() => {
    Socket.emit('user update')}, []);
  
  React.useEffect(() => {
    Socket.on('user change', setCount);
    return () => {
      Socket.off('user change', setCount);
      }
    }, []);
    
  function send_message_button(e) {
    let addMsg = userInput.current.value;
    if (addMsg === "") return;
    Socket.emit('new message', {'message': addMsg, 'user': currentUser})
    console.log('Message-user sent to server: ' + addMsg + " " + currentUser);
    userInput.current.value = null;
    e.preventDefault();
  }

  function send_message_onkey(e) {
    if (e.key === "Enter") {
      send_message_button(e);
    }
  }

  function getNewMessages() {
      React.useEffect(() => {
          Socket.on('message display', updateMsg);
          return () => {
              Socket.off('message display', updateMsg);
          }
      });
  }
    
  function updateMsg(data) {
      console.log("Received message-user from server: " + data['message'] + " " + data['user']);
      setMsg((prevUserMsg) => {
      return [...prevUserMsg, {'message': data['message'], 'user': data['user']}];
    });
  }
  
  getNewMessages();

  return (
    <>
      <h1>Chatroom</h1>
      <h1>Welcome {currentUser}!</h1>
      <h3>There are currently {userCount} users online.</h3>
      <input ref={userInput} type="text" onKeyDown={send_message_onkey} />
      <button onClick={send_message_button}>Send Message</button>
      <ul>
        <ChatLog history={userMsg} />
      </ul>
    </>
  );
}
