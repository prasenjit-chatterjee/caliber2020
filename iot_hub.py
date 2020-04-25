import random
import time
import threading
import lcd_i2c
import buzzer

from azure.iot.device import IoTHubDeviceClient, Message
from lcd_i2c import *
from buzzer import *

class iot_hub:
    # The device connection string to authenticate the device with your IoT hub.
    # Using the Azure CLI:
    # az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
    #CONNECTION_STRING = "HostName=azurecrusaders.azure-devices.net;DeviceId=CaliberDeviceId;SharedAccessKey=kT+ZzVvq76QHe4wWSKnUCEDr2jr7OziPSQ4G0hEa+t8="
    RECEIVED_MESSAGES = 0
    client= None
    lcd = None
    buzzer = None

    def __init__(self, connection_string):
        # Create an IoT Hub client
        self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self.lcd = lcd_i2c()
        self.buzzer=buzzer()

    def send_message(self, message):
        try:
            self.client.send_message(message)
            print( " Sent message: {}".format(message) )

        except KeyboardInterrupt:
            print ( "IoTHubClient stopped" )

    def message_listener(self):
        #global RECEIVED_MESSAGES
        while True:
            message = self.client.receive_message()
            iot_hub.RECEIVED_MESSAGES += 1
            print("Message received")
            response = message.data.decode().split(1)
            threads=[]
            tune=1
            if response[0]=="ECG":
                tune=1
            else:
                tune=2            

            display_thread = threading.Thread(target=self.lcd.right_to_left_scroll, args=(response[1],1,))
            display_thread.start()
            threads.append(display_thread)

            buzzer_thread = threading.Thread(target=self.buzzer.play,args=(tune,))            
            buzzer_thread.start()
            threads.append(buzzer_thread)
            
            for t in threads:
                t.join()

            # print( "    Data: {}".format(message.data) )
            # print( "    Properties: {}".format(message.custom_properties))
            # print( "    Total calls received: {}".format(iot_hub.RECEIVED_MESSAGES))

    def receive_message(self):
        try:            
            message_listener_thread = threading.Thread(target=iot_hub.message_listener, args=(self,))
            message_listener_thread.daemon = True
            message_listener_thread.start()

            while True:
                time.sleep(2)

        except KeyboardInterrupt:
            print ( "IoTHubDeviceClient sample stopped" )