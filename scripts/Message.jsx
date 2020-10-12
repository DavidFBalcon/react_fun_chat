import React from "react";
import "./Messagestyles.css"

export default function Message({ text, user, reader }) {
    function createMarkup() {
    return {__html: {text}.text};
  }

    if(user === reader){
        return (
            <div className="msg-user">
              <div className="self-tag">{user}</div>
              <div className="bubble-container ">
                <div className="bubble self">
                  {text}
                </div>
              </div>
             </div>
        );
    }
    else if(user==="Bot"){
        return(
            <div className="msg-user">
              <div className="user-tag-container-other">{user}</div>
              <div className="bubble-container">
                <div className="bubble bot" dangerouslySetInnerHTML={createMarkup()}/>
              </div>
            </div>
            );
    }
    else{
        return(
            <div className="msg-user">
              <div className="user-tag-container-other">{user}</div>
              <div className="bubble-container">
                <div className="bubble incoming">
                  {text}
                </div>
              </div>
             </div>
            );
        
    }
}
