import React, { useState, useRef } from "react";
import ChatLog from "./ChatLog";
import { v4 } from "uuid";
import { Socket } from './Socket';
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'

export default function App(props) {
  const [userMsg, setMsg] = useState([]);
  const userInput = useRef();
  const currentUser = props.username;
  
  function send_message_button(e) {
    let addMsg = userInput.current.value;
    if (addMsg === "") return;
    Socket.emit('new message', {'message': addMsg})
    console.log('Message sent to server: ' + addMsg);
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
      console.log("Received messages from server: " + data['messages']);
      setMsg((prevUserMsg) => {
      return [...prevUserMsg, data['messages']];
    });
  }
    
  getNewMessages();

  return (
    <>
      <h1>Chatroom</h1>
      <h1>Welcome {currentUser}!</h1>
      <input ref={userInput} type="text" onKeyDown={send_message_onkey} />
      <button onClick={send_message_button}>Send Message</button>
      <ul>
        <ChatLog history={userMsg} />
      </ul>
    </>
  );
}
