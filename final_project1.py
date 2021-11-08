
# Import Modules
import LocoIOT_Communicator as MSG
from IoTClient import IoTClient
import time

timer = 3
state = 0
change = 0
wait_time =0
def change_time(up, down):
    global timer
    if up == 0:
        timer = timer + 1
    else:
        timer = timer
    if down == 0 and (timer == 1 or timer ==0):
        timer = 0
    elif down == 0 and (timer != 1 or timer !=0):
        timer = timer - 1
    #print (timer)
def check_time():
    return timer
def new_time(number):
    global timer
    timer = number
def set_state(num):
    global state
    global change
    global wait_time
    wait_time = time.time()
    if num != state:
        state = num
        change = 1
def state_0():
    global state
    state = 0
        
def get_state():
    global state
    return state

try:
    
    #create message recieved over websocket
    def haveMessage(self, message):
        new_val = int(message["text1"])
        new_state =int(message["btn1"])
        
        
        set_state(new_state)
        new_time(new_val)
        
        print(message)
        
        
    # Create Message-To-Send-Over-Websocket Handling Method for IoTClient Class Instance
    def sendMessage(self):
        photo_dict = self.locoIoT.getData(self.msg.SUBTYPE_PHOTO)
        def print_butt():    
            btn_dict = [self.locoIoT.getData(self.msg.SUBTYPE_SW_4),self.locoIoT.getData(self.msg.SUBTYPE_SW_3), self.locoIoT.getData(self.msg.SUBTYPE_SW_2)]
            #print(btn_dict)
            return btn_dict
        def getState():
            if photo_dict["Photocell"] < 400:
                return 0
            else:
                return 1
        
        status_dict = {
            "Total Time(min)":check_time(),
            "TV Status": "ON",
            "Time Left (Sec)": check_time()}
        state = [getState()]
        #self.locoIoT.setData(self.msg.SUBTYPE_DO_1, state)
        passage = 0
        data = [msg.RFID_MSG_READ, 13]
        rf_dict = self.locoIoT.getData(self.msg.SUBTYPE_RFID, data)
        #print(get_change)
        #print(rf_dict)
        btn_dict = print_butt()
        
####################################################################################          
        if btn_dict[1]["Button 3"] == 0:
            for i in range(check_time()):
                data = [1]
                self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)
                time.sleep(.1)
                data = [0]
                self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)
                time.sleep(.4)
            #print("pressed")
            
        elif btn_dict[1]["Button 3"] == 1:
            data = [0]
            self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)
        
        if btn_dict[2]["Button 2"] == 0 or btn_dict[0]["Button 4"] == 0:
            data = [1]
            self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)
            time.sleep(.1)
            data = [0]
            self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)
            change_time(btn_dict[2]["Button 2"],btn_dict[0]["Button 4"])
            
        elif btn_dict[2]["Button 2"] == 1 or btn_dict[0]["Button 4"] == 1:
            data = [0]
            self.locoIoT.setData(self.msg.SUBTYPE_DO_3, data)            
####################################################################################                    
        if len(rf_dict) == 2:
            for i in range(16):
                if rf_dict["Block Data"][i] == 87:
                    passage = passage + 1
     
        
        
        if(passage == 16 or get_state() == 1) and (state[0] == 1 ):   
            state = [0]
            
        elif(passage == 16 or get_state() == 1) and (state[0] == 0):
            now_time = time.time()
            
            pulse = [1]
            full_time = 10*check_time()
            while (time.time() - now_time) < (full_time):
                if int(full_time-(time.time() - now_time))%2 == 1:
                    pulse = [1]
                    self.locoIoT.setData(self.msg.SUBTYPE_DO_2, pulse)
                elif int(full_time-(time.time() - now_time))%2 == 0:
                    pulse = [0]
                    self.locoIoT.setData(self.msg.SUBTYPE_DO_2, pulse)
                status_dict["Time Left (Sec)"] = int(full_time-(time.time() - now_time))
                self.send_message(status_dict)
                state = [0]
                
                print(int(full_time-(time.time() - now_time)))
            state = [1]
            
        
        if state[0] == 0:
            status_dict["TV Status"] = "ON"
        elif state[0] == 1:
            status_dict["TV Status"] = "OFF"
        #print(check_time())
        self.send_message(status_dict)
        
        self.locoIoT.setData(self.msg.SUBTYPE_DO_1, state)
        #print(passage)
        #print(state)
        
        #print(photo_dict)
                
######################################################################################     
    # Create IoTClient Instance with Sending (TX) Message Handling
    iotClient = IoTClient(msgRXHandler = haveMessage,msgTXHandler = sendMessage)
    # iotClient.sendDelay = 1 # Override Sending Rate - Defaults of 0.1 Seconds
    
    # Create Instance of IOT_Codes Class for Hardware Code Access
    msg = MSG.IOT_Codes()
    
    # Create IoT Settings Dictionary
    iotType = {}
    iotType["IoT"] = {"msg":msg, "USB":"/dev/ttyACM0", "sensor":[msg.SUBTYPE_DO_2,msg.SUBTYPE_DO_3, msg.SUBTYPE_SW_4, msg.SUBTYPE_SW_3, msg.SUBTYPE_SW_2,msg.SUBTYPE_RFID,msg.SUBTYPE_PHOTO,msg.SUBTYPE_DO_1]}
    # Enable IoT System with Dictionary
    iotClient.enable(iotType)
   

        
    # Create Dictionary for WebSocket Port
    enableType = {"socket port": "ws://localhost:3000"}
    # Enable WebSocket with Dictionary - Activates Blocking Code For WebSocket
    iotClient.enable(enableType)
    
    
    
    
except (KeyboardInterrupt, SystemExit):
    # Close Connections - May Take Several Seconds To Complete
    iotClient.close()