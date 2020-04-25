import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import iot_hub

from iot_hub import *

class ecg_socket():
    iot_hub= None
    retry_counter=5
    hub_message = '{{"ecg": {ecg:}}}'

    def __init__(self,connection_string):
        self.iot_hub=iot_hub(connection_string)
        self.connect()

    def on_message(self, message):
        msg_txt_formatted = self.hub_message.format(ecg=message)
        print(msg_txt_formatted)
        #self.iot_hub.send_message(msg_txt_formatted)
        

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("... Reconnecting ...")
        self.retry_counter -= 1
        if (self.retry_counter>0):
            self.connect()

    def on_open(self):
        print("Connection Open...")

    def connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://192.168.2.111:81/",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    # if __name__ == "__main__":
    #     websocket.enableTrace(True)
    #     ws = websocket.WebSocketApp("ws://192.168.2.111:81/",
    #                             on_message = on_message,
    #                             on_error = on_error,
    #                             on_close = on_close)
    #     ws.on_open = on_open
    #     ws.run_forever()