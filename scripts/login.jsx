import React, {useState, useRef} from "react";
import ReactDOM from "react-dom";
import App from "./app";

export default function Login() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setUsername] = useState("");
    const userInput = useRef();
    
    function loginUser(e) {
        let newName = userInput.current.value;
        if (newName === "") return;
        setUsername(newName);
        setLoggedIn(true);
        console.log("Passed username: ", newName);
        userInput.current.value = null;
        e.preventDefault();
      }

    function send_user_onkey(e) {
        if (e.key === "Enter") {
          loginUser(e);
        }
      }
      
      
    if(loggedIn){
        return(<App username={username} />);
    }
    else{
        return(
            <>
                <h1>Login</h1>
                <input ref={userInput} type="text" onKeyDown={send_user_onkey} />
                <button onClick={loginUser}>Login with Username</button>
            </>
            );
    }
}
