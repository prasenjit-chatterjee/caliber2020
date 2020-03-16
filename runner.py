import lcd_i2c
import dht
import therm_sensor
import iot_hub

from lcd_i2c import *
from dht import *
from therm_sensor import *
from iot_hub import *

dht = dht(26)
lcd = lcd_i2c()
iot_hub_client = iot_hub()
hub_message = '{{"roomtemperature": {temperature},"humidity": {humidity}, "bodytemperature": {bodytemperature}}}'
while True:
    dhtout = dht.get_temperature()
    therm = therm_sensor()
    scrollText="Room <> {0:0.1f}C Humidity <> {1:0.1f}% Body <> {2:0.1f}C".format(dhtout.temperature, dhtout.humidity, therm.temperature)
    msg_txt_formatted = hub_message.format(temperature=dhtout.temperature, humidity=dhtout.humidity, bodytemperature=therm.temperature)
    #lcd.right_to_left_scroll(scrollText,100)    
    #iot_hub_client.iothub_send_message(msg_txt_formatted)
    #print(scrollText)
    lcd.right_to_left_scroll(scrollText,1)