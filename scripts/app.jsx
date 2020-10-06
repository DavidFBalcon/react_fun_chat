import React, { useState, useRef } from "react";
import ChatLog from "./ChatLog";
import { v4 } from "uuid";

export default function App() {
  const [userMsg, setMsg] = useState([]);
  const userInput = useRef();

  function send_message_button(e) {
    const addMsg = userInput.current.value;
    if (addMsg === "") return;
    setMsg((prevUserMsg) => {
      return [...prevUserMsg, { id: v4(), plaintext: addMsg }];
    });
    userInput.current.value = null;
  }

  function send_message_onkey(e) {
    if (e.key === "Enter") {
      send_message_button(e);
    }
  }

  return (
    <>
      <h1>Prototype Terminator</h1>
      <input ref={userInput} type="text" onKeyDown={send_message_onkey} />
      <button onClick={send_message_button}>Send Message</button>
      <ul>
        <ChatLog history={userMsg} />
      </ul>
    </>
  );
}
