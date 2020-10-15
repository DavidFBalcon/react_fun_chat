import React from "react";
import "./Messagestyles.css"
import botpfp from './botpfp.png';

export default function Message({ text, user, reader, pfp_url }) {
    function createMarkup() {
    return {__html: {text}.text};
  }
    function createImg(){
      return {__html: {pfp_url}.pfp_url};
    }

    if(user === reader){
        return (
            <div className="msg-user">
            
              <div className="user-pfp-self">
                <div className="pfp" dangerouslySetInnerHTML={createImg()}/><div className="self-tag">{user}</div>
              </div>
            
              <div className="clear"> </div>
              <div className="bubble-container ">
                <div className="bubble self" dangerouslySetInnerHTML={createMarkup()}/>
              </div>
             </div>
        );
    }
    else if(user==="Bot"){
        return(
            <div className="msg-user">
            
              <div className="user-pfp-other">
                <div className="pfp"><img src={botpfp} /></div><div className="user-tag-container-other">Paimon (Emergency Food) [Bot]</div>
              </div>
              
              <div className="bubble-container">
                <div className="bubble bot" dangerouslySetInnerHTML={createMarkup()}/>
              </div>
            </div>
            );
    }
    else{
        return(
            <div className="msg-user">
            
              <div className="user-pfp-other">
                <div className="pfp" dangerouslySetInnerHTML={createImg()}/><div className="user-tag-container-other">{user}</div>
              </div>
              
              <div className="bubble-container">
                <div className="bubble incoming" dangerouslySetInnerHTML={createMarkup()}>
                </div>
              </div>
             </div>
            );
        
    }
}
