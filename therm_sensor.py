from w1thermsensor import W1ThermSensor
 
body_temp_sensor = W1ThermSensor()

class therm_sensor:
    bodyTempSensor = W1ThermSensor()
    temperature = 4.0

    def __init__(self):        
        self.temperature = body_temp_sensor.get_temperature()
    