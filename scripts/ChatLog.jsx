import React from "react";
import Message from "./Message";

export default function ChatLog({ history }) {
  return history.map((MsgElement) => {
    return <Message input={MsgElement.plaintext} key={MsgElement.id} />;
  });
}
