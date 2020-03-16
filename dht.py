import Adafruit_DHT

class dht:
    #DHT11 reading
    sensor = Adafruit_DHT.DHT22
    input_pin = 26

    def __init__(self, dht_pin):
        dht.input_pin=dht_pin

    def get_temperature(self):
        self.humidity, self.temperature = Adafruit_DHT.read(dht.sensor, dht.input_pin)
        if self.humidity is not None and self.temperature is not None:
            dhtoutput = dht_io_model(self.humidity, self.temperature)
            return dhtoutput
        else:
            return dht_io_model(0, 0)

class dht_io_model:
    humidity = 0.0
    temperature = 0.0

    def __init__(self, humidity, temperature):
        self.humidity = humidity
        self.temperature = temperature

    def values(self):
        return self