import React from "react";
import "./Messagestyles.css"

export default function Message({ input, user, reader }) {
    if(user === reader){
        return (
            <div class="msg-user">
              <div class="self-tag">{user}</div>
              <div class="bubble-container ">
                <div class="bubble self">
                  {input}
                </div>
              </div>
             </div>
        );
    }
    else if(user==="Bot"){
        return(
            <div class="msg-user">
              <div class="user-tag-container-other">{user}</div>
              <div class="bubble-container">
                <div class="bubble bot">
                  {input}
                </div>
              </div>
            </div>
            );
    }
    else{
        return(
            <div class="msg-user">
              <div class="user-tag-container-other">{user}</div>
              <div class="bubble-container">
                <div class="bubble incoming">
                  {input}
                </div>
              </div>
             </div>
            );
        
    }
}
