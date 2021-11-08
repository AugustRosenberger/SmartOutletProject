// Button State and WebSocket Variables
var state = 0;
var socket = null;
var stateStrs = ["Send Password", "Set Time"];
var socketStr = "ws://localhost:3000";

// Run On Load
window.addEventListener("DOMContentLoaded", function() {
    resetWebsocket();
}, false);


// Create WebSocket Connection and WebSocket Event Handling Functions
function resetWebsocket() {

  if (socket) {
      socket.close();
  }

  // Create WebSocket Object
  socket = new WebSocket(socketStr);

  // On WebSocket Connection Opened
  socket.onopen = function() {
    console.log("Opened Connection");
  }

  // On WebSocket Connection Closed
  socket.onclose = function() {
    console.log("Closed Connection");
  }

  // On Message Received
  socket.onmessage = function(event) {
      // Parse Received JSON Message
      var obj = JSON.parse(event.data);            
      // Convert Message Object to String
      var str = JSON.stringify(obj, null);
      // Set Text on WebPage as String Message
      document.getElementById("dataid").innerHTML = str;
  }
  
}

// Handle Button Presses
function updateState() {
    // Toggle Variable "state"
    state = 1 - state;
    // Update Text on Button
    //updateBtnLabel();
    // Create JSON for Message and Send Over WebSocket Connection
    var obj = {"btn1":state};
    var msgStr = JSON.stringify(obj);
    socket.send(msgStr);
}

// On Button Press
function sendMessage() {
    // Toggle Variable "state"
    state = 1 - state;
    // Update Text on Button
   // updateBtnLabel();
    // Get Text From Input Text Field
    var textStr = document.getElementById("text1").value;
    var btnstate = state;
 // Create Dictionary Object and Convert to JSON String
    var obj = {"btn1":btnstate,"text1":textStr};
    var msgStr = JSON.stringify(obj);
    // Send JSON Over Socket
    socket.send(msgStr);
}

// Update Text on Button Function
function updateBtnLabel() {
    document.getElementById("btn2").innerHTML = stateStrs[state];
}



