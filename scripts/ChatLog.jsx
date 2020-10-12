import React from "react";
import Message from "./Message";

export default function ChatLog({ history, reader }) {
  return history.map((MsgElement, index) => {
    return <Message input={MsgElement.message} user={MsgElement.user} key={index} reader={reader} />;
  });
}