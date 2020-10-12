import React from "react";
import "./Messagestyles.css"

export default function Message({ input, user, reader }) {
    if(user === reader){
        return (
            <div className="sentMessage">
                <div className="user_box">
                    <p className="selfText">{user}</p>
                </div>
                <p className="contentText">{input}</p>
            </div>
        );
    }
    else if(user==="Bot"){
        return(
            <div className="readMessage">
                <div className="bot_box">
                    <p className="userText">{user}</p>
                </div>
                <p className="contentText">{input}</p>
            </div>
            );
    }
    else{
        return(
            <div className="readMessage">
                <div className="reader_box">
                    <p className="userText">{user}</p>
                </div>
                <p className="contentText">{input}</p>
            </div>
            );
        
    }
}
