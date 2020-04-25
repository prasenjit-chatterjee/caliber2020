#import lcd_i2c
import therm_sensor
import iot_hub
import threading
import gyro
import pulse_sensor
import ecg_socket

from pulse_sensor import *
from gyro import *
from therm_sensor import *
from iot_hub import *
from ecg_socket import *

CalibreGyroDevice = "HostName=azurecrusaders.azure-devices.net;DeviceId=CalibreGyroDevice;SharedAccessKey=pzuBw18h8m46KTz4HbKpj3GnKppYuWizTVQDUB+MmWc="
CalibreECGDevice = "HostName=azurecrusaders.azure-devices.net;DeviceId=CalibreECGDevice;SharedAccessKey=YFghzoPgF8PS4Bb3Yan5A3FikZvL+gnxn5cTiaCjWyk="
CalibrePulseDevice = "HostName=azurecrusaders.azure-devices.net;DeviceId=CalibrePulseDevice;SharedAccessKey=DGUDl7AqZBqgOkp2wjjlsG4tvcdeF261+AYsgvQncJw="
CaliberDeviceId = "HostName=azurecrusaders.azure-devices.net;DeviceId=CaliberDeviceId;SharedAccessKey=kT+ZzVvq76QHe4wWSKnUCEDr2jr7OziPSQ4G0hEa+t8="

#lcd = lcd_i2c()
iot_hub_client = iot_hub(CaliberDeviceId)
motion=gyro(CalibreGyroDevice)
bpm=pulse(CalibrePulseDevice)
therm=therm_sensor(CaliberDeviceId)

while True:
    threads=[]

    motion_thread = threading.Thread(target=motion.post_to_iot_hub)            
    motion_thread.start()
    threads.append(motion_thread)

    pulse_thread = threading.Thread(target=bpm.read_pulse)            
    pulse_thread.start()
    threads.append(pulse_thread)

    ecg_thread = threading.Thread(target=ecg_socket, args=(CalibreECGDevice,))
    ecg_thread.start()
    threads.append(ecg_thread)

    therm_thread = threading.Thread(target=therm.post_to_iot_hub)            
    therm_thread.start()
    threads.append(therm_thread)

    receiver_thread = threading.Thread(target=iot_hub_client.message_listener)            
    receiver_thread.start()
    threads.append(receiver_thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("Exiting Main Thread")

    #lcd.right_to_left_scroll(scrollText,100)    
    #iot_hub_client.iothub_send_message(msg_txt_formatted)
    #print(scrollText)



# ff='{{"gyro":{{"Gx":{Gx:0.3f},"Gy":{Gy:0.3f},"Gz":{Gz:0.3f},"Ax":{Ax:0.3f},"Ay":{Ay:0.3f},"Az":{Az:0.3f}}}}}'
# hub_message = '{{"roomtemperature": {temperature},"humidity": {humidity}, "bodytemperature": {bodytemperature}}}'
# uu=hub_message.format(temperature=0, humidity=0, bodytemperature=0)
# fss=ff.format(Gx=555.555555555,Gy=555.555555555,Gz=0,Ax=0,Ay=0,Az=555.555555555)
# print(fss)