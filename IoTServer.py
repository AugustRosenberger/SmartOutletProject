from websocket_server import WebsocketServer
import threading
import time

class IoTServer:

    def __init__ (self, portNum):
        self.connected = False
        self.serverThread = threading.Thread(target = self.begin, args = (portNum, ))
        self.serverThread.daemon = True
        self.serverThread.start()
        
    def begin(self, portNum):
        
        self.server = WebsocketServer(portNum) 
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.connected = True
        self.server.run_forever()
        
    # Called for every client connecting
    def new_client(self, client, server):
        pass
    
    # Called for every client disconnecting
    def client_left(self, client, server):
        pass
    
    # Called when a client sends a message
    def message_received(self, client, server, message):
        # loop through all connected clients
        # and send the message to all clients but the one that sent the message
        for c in server.clients:
            if c['id'] != client['id']:
                self.server.send_message(c, message)
        
    def close_server(self):
        if (self.server is not None):
            self.server.shutdown()
            self.server.server_close()


if __name__ == "__main__":
    
    try:
        iotServer = IoTServer(3000)
        #iotServer = IoTServer(3000, '0.0.0.0')
        
        while (iotServer.connected == False):
            time.sleep(1)
    
        while (iotServer.connected == True):
            time.sleep(1)
            
        iotServer.server.server_close()
            
    except (KeyboardInterrupt, SystemExit):
        if (iotServer.server is not None):
            iotServer.server.server_close()
        