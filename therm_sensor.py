import iot_hub
import dht

from dht import *
from iot_hub import *
from w1thermsensor import W1ThermSensor
 

class therm_sensor:
    body_temp_sensor = None
    temperature = 4.0
    iot_hub= None
    dht = None
    hub_message = '{{"roomtemperature": {temperature},"humidity": {humidity}, "bodytemperature": {bodytemperature}}}'

    def __init__(self, connection_string):
        self.iot_hub=iot_hub(connection_string)
        self.dht = dht(26)
        self.body_temp_sensor = W1ThermSensor()
        #self.temperature = body_temp_sensor.get_temperature()
    
    def post_to_iot_hub(self):
        dhtout = self.dht.get_temperature()
        msg_txt_formatted = self.hub_message.format(roomtemperature=dhtout.temperature, humidity=dhtout.humidity, bodytemperature=self.body_temp_sensor.get_temperature())
        self.iot_hub.send_message(msg_txt_formatted)

        