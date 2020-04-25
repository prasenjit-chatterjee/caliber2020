'''
    Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import smbus			#import SMBus module of I2C
import iot_hub

from time import sleep          #import
from iot_hub import *

class gyro():
		
	#some MPU6050 Registers and their Address
	PWR_MGMT_1   = 0x6B
	SMPLRT_DIV   = 0x19
	CONFIG       = 0x1A
	GYRO_CONFIG  = 0x1B
	INT_ENABLE   = 0x38
	ACCEL_XOUT_H = 0x3B
	ACCEL_YOUT_H = 0x3D
	ACCEL_ZOUT_H = 0x3F
	GYRO_XOUT_H  = 0x43
	GYRO_YOUT_H  = 0x45
	GYRO_ZOUT_H  = 0x47
	TEMP = 0x41

	bus = smbus.SMBus(1) 	# or bus = smself.SMBus(0) for older version boards
	Device_Address = 0x68   # MPU6050 device address
	iot_hub=None
	hub_message = '{{"gyro":{{"Gx":{Gx:0.3f},"Gy":{Gy:0.3f},"Gz":{Gz:0.3f},"Ax":{Ax:0.3f},"Ay":{Ay:0.3f},"Az":{Az:0.3f}}}}}'

	def get_tempxo(self):
		tempRow= self.read_raw_data(self.TEMP)
		tempC=(tempRow / 340.0) + 36.53
		tempC="%.2f" %tempC
		print(tempC)
		#setCursor(0,0)
		print("Temp: ")
		print(str(tempC))
		sleep(.2)


	def MPU_Init(self):
		#write to sample rate register
		self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
		
		#Write to power management register
		self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)
		
		#Write to Configuration register
		self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
		
		#Write to Gyro configuration register
		self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
		
		#Write to interrupt enable register
		self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)

	def read_raw_data(self, addr):
		#Accelero and Gyro value are 16-bit
		high = self.bus.read_byte_data(self.Device_Address, addr)
		low = self.bus.read_byte_data(self.Device_Address, addr+1)

		#concatenate higher and lower value
		value = ((high << 8) | low)
		
		#to get signed value from mpu6050
		if(value > 32768):
				value = value - 65536
		return value

	def __init__(self, connection_string):
		self.iot_hub = iot_hub(connection_string)        
		self.MPU_Init()
		#self.get_tempxo()

	

	def read_data(self):
		#Read Accelerometer raw value
		acc_x = self.read_raw_data(self.ACCEL_XOUT_H)
		acc_y = self.read_raw_data(self.ACCEL_YOUT_H)
		acc_z = self.read_raw_data(self.ACCEL_ZOUT_H)
		
		#Read Gyroscope raw value
		gyro_x = self.read_raw_data(self.GYRO_XOUT_H)
		gyro_y = self.read_raw_data(self.GYRO_YOUT_H)
		gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
		
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0
		
		Gx = gyro_x/131.0
		Gy = gyro_y/131.0
		Gz = gyro_z/131.0
			
		msg_txt_formatted = self.hub_message.format(Gx=Gx,Gy=Gy,Gz=Gz,Ax=Ax,Ay=Ay,Az=Az)
		return msg_txt_formatted
		#print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)    
		#sleep(1)

	def post_to_iot_hub(self):
		while True:
			result = self.read_data()
			print(result)
			self.iot_hub.send_message(result)