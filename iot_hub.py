import random
import time
import threading

from azure.iot.device import IoTHubDeviceClient, Message

class iot_hub:
    # The device connection string to authenticate the device with your IoT hub.
    # Using the Azure CLI:
    # az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
    #CONNECTION_STRING = "HostName=azurecrusaders.azure-devices.net;DeviceId=CaliberDeviceId;SharedAccessKey=kT+ZzVvq76QHe4wWSKnUCEDr2jr7OziPSQ4G0hEa+t8="
    RECEIVED_MESSAGES = 0
    client= None

    def __init__(self, connection_string):
        # Create an IoT Hub client
        self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)        

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
            print( "    Data: {}".format(message.data) )
            print( "    Properties: {}".format(message.custom_properties))
            print( "    Total calls received: {}".format(iot_hub.RECEIVED_MESSAGES))

    def receive_message(self):
        try:            
            message_listener_thread = threading.Thread(target=iot_hub.message_listener, args=(self,))
            message_listener_thread.daemon = True
            message_listener_thread.start()

            while True:
                time.sleep(2)

        except KeyboardInterrupt:
            print ( "IoTHubDeviceClient sample stopped" )