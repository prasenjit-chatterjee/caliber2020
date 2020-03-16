import iot_hub
from iot_hub import *

iot_hub_client = iot_hub()

while True:
    iot_hub_client.iothub_receive_message() 