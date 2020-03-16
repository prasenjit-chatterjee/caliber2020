import random
import time
import threading

from azure.iot.device import IoTHubDeviceClient, Message

class iot_hub:
    # The device connection string to authenticate the device with your IoT hub.
    # Using the Azure CLI:
    # az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
    CONNECTION_STRING = "HostName=azurecrusaders.azure-devices.net;DeviceId=CaliberDeviceId;SharedAccessKey=kT+ZzVvq76QHe4wWSKnUCEDr2jr7OziPSQ4G0hEa+t8="
    RECEIVED_MESSAGES = 0

    def iothub_client_init(self):
        # Create an IoT Hub client
        client = IoTHubDeviceClient.create_from_connection_string(iot_hub.CONNECTION_STRING)
        return client

    def iothub_send_message(self, message):
        try:
            client = iot_hub.iothub_client_init(self)            
            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            #time.sleep(3)

        except KeyboardInterrupt:
            print ( "IoTHubClient stopped" )

    def message_listener(self, client):
        #global RECEIVED_MESSAGES
        while True:
            message = client.receive_message()
            iot_hub.RECEIVED_MESSAGES += 1
            print("Message received")
            print( "    Data: {}".format(message.data) )
            print( "    Properties: {}".format(message.custom_properties))
            print( "    Total calls received: {}".format(iot_hub.RECEIVED_MESSAGES))

    def iothub_receive_message(self):
        try:
            client = IoTHubDeviceClient.create_from_connection_string(iot_hub.CONNECTION_STRING)
            message_listener_thread = threading.Thread(target=iot_hub.message_listener, args=(self,client,))
            message_listener_thread.daemon = True
            message_listener_thread.start()

            while True:
                time.sleep(2)

        except KeyboardInterrupt:
            print ( "IoTHubDeviceClient sample stopped" )