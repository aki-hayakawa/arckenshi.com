// var projectID = prompt("Please enter your project ID:");
// console.log(projectID);
// if (projectID === null || projectID.trim() === "") {
//     alert("Project ID cannot be empty. Please try again.");
// } else {
//     projectID = parseInt(projectID);
//     if (isNaN(projectID)) {
//         alert("Project ID must be a number. Please try again by refreshing the page.");
//     } else {
//     }
// }

var mqtt;
var reconnectTimeout = 3000;
var host="service.redtone.com"; //change this
var port=8083;
var flag_connected = false;

function onFailure(message) {
    console.log("Connection Attempt to Host "+host+"Failed");
    alert("Failed to connect to machine!");
    setTimeout(MQTTconnect, reconnectTimeout);
}

function onMessageArrived(msg){
    // console.log(msg.payloadString);
    let dataList = JSON.parse(msg.payloadString)['d'];
    for (let i=0; i<dataList.length; i++){
        try{
            let data = dataList[i];
            let pid = data['pid'];
            let value = data['v'];
            // console.log(pid);
            // console.log(value);
            let element = document.getElementById(pid);
            if(element != null || element != undefined){
                if (element.classList.contains('isSwitch')) {
                    if(value.toString() == "1"){
                        element.checked = true;
                    }
                    if(value.toString() == "0"){
                        element.checked = false;
                    }
                }
                element.value = value.toString();
            }
        }
        catch(err){
            console.log(err);
        }
  
    }
}

function onConnectionLost(responseObject) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
    if (responseObject.errorCode !== 0) {
        flag_connected = false;
        $("#disconnectedModal").modal("show");
        document.getElementById("onlineStatus").classList.remove("hide");
    }
  }

function onConnect() {
    console.log("Connected");
    flag_connected = true;
    mqtt.subscribe(`/usr/plcnet/www/bysz/com/${projectID}/edge/u`);
    // document.getElementsByClassName("preloader")[0].style.display = "block";
    getGroupValue("Manual");
}

function MQTTconnect() {
    console.log("Connecting to "+ host +" "+ port);
    var x=Math.floor(Math.random() * 10000000000); 
    var cname="riotClient-"+x;
    mqtt = new Paho.MQTT.Client(host,port,cname);
    // let useSSL = false;
    // if (document.location.protocol === 'https:') {
    //     useSSL = true;
    // }
    // else{
    //     useSSL = false;
    // }

    var options = {
        timeout: 3,
        useSSL:true,
        onSuccess: onConnect,
        onFailure: onFailure,
    };

    mqtt.onMessageArrived = onMessageArrived;
    mqtt.onConnectionLost = onConnectionLost;

    mqtt.connect(options);
}

MQTTconnect();

function handleChange(x) {
    let elementValue = x.value.toString();
    if (flag_connected == false){
        alert("You are disconnected! Any buttons or values pressed/changed will not be applied to the machine!");
        return;
    }
    if (x.classList.contains('page-indicator')) {
        let group = x.classList[x.classList.length - 1].replace("page-indicator-","");
        changePageIndicator(x);
        getGroupValue(group);
        return;
    }
    if (x.classList.contains('isSwitch')) {
        if(x.checked == true){
            elementValue = "1";
        }else{
            elementValue = "0";
        }
    }

    // if(x.id.includes("Automation")) {
    //     if(x.checked ==true) {
    //         state = 1
    //     } else {
    //         state = 0
    //     }
    // } else {
    //     state = x.value
    // }

    let sendMessage = {"d":[{"pid":x.id.toString(),"sid":"ModbusTCP","v":elementValue}],"f":"s"};

    message = new Paho.MQTT.Message(JSON.stringify(sendMessage));
    message.destinationName = `/usr/plcnet/www/bysz/com/${projectID}/edge/d`;
    try{
        mqtt.send(message);
    }
    catch(err){
        // console.log(err);
        console.log("Error sending message");
    }
}

function changeTab(x) {
    // document.getElementsByClassName("preloader")[0].style.display = "block";
    let group = x.name.toString().replace("navpill-","");
    getGroupValue(group);
}

function changePageIndicator(pageIndicator){
    let message = null;

    let padeIndicatorMessage = {"d":[{"pid":pageIndicator.id.toString(),"sid":"ModbusTCP","v":pageIndicator.value.toString()}],"f":"s"}
    message = new Paho.MQTT.Message(JSON.stringify(padeIndicatorMessage));
    message.destinationName = `/usr/plcnet/www/bysz/com/${projectID}/edge/d`;
    try{
        mqtt.send(message);
    }
    catch(err){
        // console.log(err);
        console.log("Error sending message");
    }
}

function getGroupValue(group){
    $("#boyunMQTTValueGetBackStatusModal").modal("show");
    let index = 0;
    let counter = 0;
    let newestValueMessage = {"d":[],"f":"q"};
    let message = null;

    let groupArray = Array.from(document.getElementsByClassName("all-input-"+group));
    groupArray.forEach(element => {
        element.value = "";
        
        newestValueMessage.d.push({"pid":element.id.toString(),"sid":"ModbusTCP"});

        if (counter >= 5 || index == groupArray.length - 1){
            message = new Paho.MQTT.Message(JSON.stringify(newestValueMessage));
            message.destinationName = `/usr/plcnet/www/bysz/com/${projectID}/edge/d`;
            try{
                mqtt.send(message);
            }
            catch(err){
                // console.log(err);
                console.log("Error sending message");
            }

            newestValueMessage = {"d":[],"f":"q"};
            message = null;
            counter = 0;
        }

        counter = counter + 1;
        index = index + 1;
    });
}

// function send_message(event) {
//     // event.preventDefault();
//     event.append('requesttime1', Math.floor(Date.now() / 1000));
//     const data = {};
//     event.forEach((value, key) => (data[key] = value));

//     console.log(JSON.stringify(data));

//     message = new Paho.MQTT.Message(JSON.stringify(data));
//     message.destinationName = "/hydroponic/{{session.siteid}}/update"
//     mqtt.send(message);
// }

// var mqttOnline;
// function onFailureOnline(message) {
//     console.log("Connection Attempt to Online MQTT server "+host+"Failed");
//     setTimeout(MQTTOnlineconnect, reconnectTimeout);
// }

// function onMessageArrivedOnline(msg){
//     let isOnline = JSON.parse(msg.payloadString)["isOnline"];
//     let onlineStatusIconSpan = document.getElementById("onlineStatusIconSpan");
//     let onlineStatusSpan = document.getElementById("onlineStatusSpan");
//     if(isOnline == true){
//         if(onlineStatusIconSpan.classList.contains("danger")){
//             onlineStatusIconSpan.classList.remove("danger");
//         }
//         onlineStatusSpan.innerHTML = "Device is Online";
//     }
//     else{
//         if(!onlineStatusIconSpan.classList.contains("danger")){
//             onlineStatusIconSpan.classList.add("danger");
//         }
//         onlineStatusSpan.innerHTML = "Device is Offline";
//     }
// }

// function onConnectOnline() {
//     console.log("Connected to Online MQTT server");
//     mqttOnline.subscribe("/heart/www/bysz/com/1123/isonline");
// }

// function MQTTOnlineconnect() {
//     console.log("Connecting to Online MQTT server "+ host +" "+ port);
//     var x=Math.floor(Math.random() * 10000000000); 
//     var cname="riotClient-"+x;
//     mqttOnline = new Paho.MQTT.Client(host,port,cname);
//     var options = {
//         userName : "mqtt",
//         password : "mqtt",
//         timeout: 3,
//         useSSL:false,
//         onSuccess: onConnectOnline,
//         onFailure: onFailureOnline,
//     };

//     mqttOnline.onMessageArrived = onMessageArrivedOnline;

//     mqttOnline.connect(options);
// }

// MQTTOnlineconnect();