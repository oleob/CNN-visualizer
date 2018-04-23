import React from 'react';
import ReactDOM from 'react-dom';
import App from './App'

// const socket = io.connect('http://' + document.domain + ':' + location.port);
//
// socket.on('connect', () => {
//   socket.emit('connected', {data: 'I\'m connected!'});
// });
// socket.on('message', (message)=>{
//   console.log(message)
// });


ReactDOM.render(<App />, document.getElementById("root"));
