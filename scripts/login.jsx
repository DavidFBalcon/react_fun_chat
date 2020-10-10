import React, {useState} from "react";
import ReactDOM from "react-dom";
import App from "./app";

export default function login() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setUsername] = useState("");
    if(loggedIn){
        return(<App username={username} />);
    }
    else{
        return(<Login setUsername={setUsername} setLoggedIn={setLoggedIn} />);
    }
}
