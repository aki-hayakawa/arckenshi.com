var isConnected = true;
var socket;
$(document).ready(function(){
	var startLink = "";
	if (document.location.protocol === 'https:') {
		startLink = "wss";
	}
	else{
		startLink = "ws";
	}
	socket = new WebSocket(startLink + '://' + location.host + '/echo');

	  function updateCount() {
		if(socket.readyState === socket.OPEN){
			if (document.visibilityState === 'visible') {
				// console.log("Page is in the foreground");
				console.log("Im still alive");
				socket.send("Im still alive");
			} else if (document.visibilityState === 'hidden') {
				// console.log("Page is in the background");
			}
			try{
				let counter = document.getElementById("counter");
				counter.innerHTML = parseInt(counter.innerHTML) + 1;
			}
			catch(err){
			}
		}
		if(socket.readyState === socket.CLOSING || socket.readyState === socket.CLOSED){
			isConnected = false;
			try{
				let socketStatus = document.getElementById("socketStatus");
				socketStatus.innerHTML = "Connection cut";
			}
			catch(err){
			}
		}
	  }

	  setInterval(updateCount, 1000);
  
	  socket.addEventListener('message', ev => {
	     const obj = JSON.parse(ev.data);
		//  console.log(obj);
		//  function closeSocket(){
		// 	socket.close();
		//  }

		//  setTimeout(closeSocket, 10000);
                	if(obj.type=='OnOff') 
                	{
                		
						if(obj.name.includes("ControlMode") && obj.name.includes("DedicatedRelay")){
							document.getElementsByName(obj.name.toString()).forEach((element) => {
								if(element.value == obj.state){
									element.checked = true;
								}
							})
						}
						else{
							if(obj.state=='ON')
							{
									$('#'+obj.name+'').prop("checked", true);
									//if($('#'+obj.name+'').bootstrapSwitch('state')==false) {
									//	$('#'+obj.name+'').bootstrapSwitch('state', true);
									//}
	
	
									$('#on_'+obj.name+'').removeClass('hide');
									$('#off_'+obj.name+'').addClass('hide');
	
	
	
	
	
								
							} else {
								$('#'+obj.name+'').prop("checked", false);
								//if($('#'+obj.name+'').bootstrapSwitch('state')==true) {
								//	$('#'+obj.name+'').bootstrapSwitch('state', false);
								//}                			
	
										$('#off_'+obj.name+'').removeClass('hide');
										$('#on_'+obj.name+'').addClass('hide');
	
							}
						}

                		
                		//if($('#'+obj.name+'').bootstrapSwitch('state')==false) {
                		//	$('#'+obj.name+'').bootstrapSwitch('state', true);
                		//}
                		//$('#'+obj.name+'').prop("checked", true);
                		
                	
                	}	else if(obj.type=='Decimal' || obj.type=='Quantity') {    
                		
                		
										if(obj.name.includes("Water_EC") || obj.name=='Water_EC' || obj.name=='Water_EC1' || obj.name=='Water_EC2') {
											n=parseFloat(obj.state).toFixed(2);
										}
										else {
											n=obj.state;
										}
                		          		
                		$('#'+obj.name+'').val(''+n+'');
                		$('#'+obj.name+'').html(''+n+'');
                	} else if(obj.type == 'String'){
						try{
							if (document.getElementById(obj.name).type === "radio"){
								document.getElementsByName(obj.name).forEach((element) => {
									if(element.value === obj.state){
										element.checked = true;
									}
								});
							}
							else{
								$('#'+obj.name+'').val(''+obj.state+'');
								$('#'+obj.name+'').html(''+obj.state+'');
							}
						}
						catch(err){
							$('#'+obj.name+'').val(''+obj.state+'');
							$('#'+obj.name+'').html(''+obj.state+'');
						}
					}else if(obj.type == 'KYS'){
									// socket.onclose = function () {};
									isConnected = false;
									console.log("KYS");
									socket.close();
									$("#disconnectedModal").modal("show");
									// alert("Please Refresh Page to Get the Latest Data from Site");
									// location.reload();
					}else {
                		
										if(obj.name.includes("Water_EC") || obj.name=='Water_EC' || obj.name=='Water_EC1' || obj.name=='Water_EC2') {
											n=parseFloat(obj.state).toFixed(2);
										}
										else {
											n=obj.state;
										}
                		$('#'+obj.name+'').html(''+obj.state+'');
                	}
                	
                	



	  });


});

function ClickChange(input) {
	if(input.name === "placeHolder" || input.name === "SiteName"){
		return;
	}
    if(!isConnected){
          return;
    }

    $.ajax({
        type: "GET",
        url: "/apis",
        data: { 
            action:'update',
            state:input.value,
            item:input.name
        },
        success: function(result) {
            //alert('ok');
            //alert(result);
        },
        error: function(result) {
            //alert('error');
        }
    });


}	
 
function handleChange(checkbox) {
	var status = "";
    if (checkbox.checked == true) 
		{
			 id=checkbox.id;
			 status="ON";
       checkbox.checked = false;
    }
    else
    {
      id=checkbox.id;
      status="OFF";
      checkbox.checked = true;
		}
    
	if(checkbox.id === "placeHolder" || checkbox.id === "SiteName"){
		return;
	}
    if(!isConnected){
        return;
    }
    
    $.ajax({
        type: "GET",
        url: "/apis",
        data: { 
            action:'update',
            state:status,
            item:id
        },
        success: function(result) {
            //alert('ok');
            //alert(result);
        },
        error: function(result) {
            //alert('error');
        }
    });

 
}	


$(document).on('change','input',function(e) {
  e.preventDefault();
  if(this.value === "on" || this.value === "off"){
      return
  }
  if(this.id === "placeHolder" || this.id === "SiteName"){
	return;
  }
  if(!isConnected){
    if(!this.step){
      return
    }
    try{
      // console.log("Conn default " + this.defaultValue.toString());
      // console.log("Conn value " + this.value.toString());
      document.querySelectorAll('input').forEach((element) => {
        if(element.id.includes(this.id+"_")){
          element.value = this.defaultValue;
        }
      })
    }
    catch(err){
      // console.log(err);
    }
    return
  }
  $.ajax({
      type: "GET",
      url: "/apis",
      data: { 
          action:'update',
          state:$(this).val(),
          item:$(this).attr('id')
      },
      success: function(result) {
          //alert('ok');
          //alert(result);
      },
      error: function(result) {
          //alert('error');
      }
  });
  this.defaultValue = this.value;
});



      let inactivityTime = function() {
        let time;
        window.onload = resetTimer;
        document.onmousemove = resetTimer;
        document.onkeypress = resetTimer;
        function logout() {
         // alert("You are now logged out.")
          window.location = "/logout";
        }
        function resetTimer() {
          clearTimeout(time);
          time = setTimeout(logout, 900000)
        }
      };
      window.onload = function() {
        inactivityTime();
      }

	//   window.onbeforeunload = function() {
	// 	socket.onclose = function () {}; // disable onclose handler first
	// 	// console.log("Socket Closed via onbeforeunload");
	// 	socket.close();
	//   };

	//   window.addEventListener("unload", function () {
	// 	if(socket.readyState == WebSocket.OPEN){
	// 		// console.log("Socket Closed via unload");
	// 		socket.onclose = function () {};
	// 		socket.close();
	// 	}
	//   });



//setTimeout(function(){
//   window.location.reload();
//}, 30000);


