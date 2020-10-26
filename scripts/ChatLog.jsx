import React from 'react';
import Message from './Message';

export default function ChatLog({ history, reader }) {
  return history.map((MsgElement, index) => <Message text={MsgElement.message} user={MsgElement.user} key={index} reader={reader} pfp_url={MsgElement.pfp_url} />);
}
