document.onkeydown = updateKey;
document.onkeyup = resetKey;
const net = require('net');
var server_camera_port = 9000;
var server_port = 65432;
var server_addr = "192.168.86.206";   // the IP address of your Raspberry PI
const piClient = net.createConnection({ port: server_port, host: server_addr })


function register(){
    console.log("to register ", piClient)
    piClient.on('connect', () => {
        console.log('connected to pi server!');
    });
    // get the data from the server
    piClient.on('data', (data) => {
        //document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        var obj = JSON.parse(data);
        console.log(obj);
   
        document.getElementById("temperature").innerHTML = obj.temp;
        document.getElementById("speed").innerHTML = obj.speed
        document.getElementById("distance").innerHTML = obj.distance;
   
    });

    piClient.on('end', () => {
        console.log('disconnected from pi server');
    });
    registerCamera()
}


// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_data(value){
 //   setInterval(function(){
        // get image from python server
        //client(value);
        piClient.write(value);
   // }, 50);
}
