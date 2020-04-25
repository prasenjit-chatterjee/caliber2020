import Adafruit_ADS1x15
import serial
import time
import iot_hub

from iot_hub import *

class pulse(object):

  rate = [0]*10
  amp = 100
  GAIN = 2/3  
  curState = 0
  stateChanged = 0
  iot_hub=None
  hub_message = '{{"bpm": {bpm:0.1f}}}'
  # ser = serial.Serial ("/dev/ttyS0", 9600)

  # def send_to_prcessing(prefix, data):
  #     ff=prefix.encode()
  #     ser.write(ff)
  #     ser.write(str(data).encode())
  #     ser.write("\n".encode())

  def __init__(self, connection_string):
    self.iot_hub=iot_hub(connection_string)

  def post_to_iot_hub(self,bpm):    
    msg_txt_formatted = self.hub_message.format(bpm=bpm)
    print(msg_txt_formatted)
    self.iot_hub.send_message(msg_txt_formatted)

  def read_pulse(self):
      firstBeat = True
      secondBeat = False
      sampleCounter = 0
      lastBeatTime = 0
      lastTime = int(time.time()*1000)
      th = 525
      P = 512
      T = 512
      IBI = 600
      Pulse = False
      adc = Adafruit_ADS1x15.ADS1015()  
      while True:
          
          Signal = adc.read_adc(0, gain=self.GAIN)   
          curTime = int(time.time()*1000)
          # send_to_prcessing("S",Signal)
          sampleCounter += curTime - lastTime
          lastTime = curTime
          N = sampleCounter - lastBeatTime

          if Signal > th and  Signal > P:          
              P = Signal
      
          if Signal < th and N > (IBI/5.0)*3.0 :  
              if Signal < T :                      
                T = Signal                                                 
          
          if N > 250 :                              
              if  (Signal > th) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
                Pulse = 1
                IBI = sampleCounter - lastBeatTime
                lastBeatTime = sampleCounter       

                if secondBeat :                     
                  secondBeat = 0
                  for i in range(0,10):             
                    self.rate[i] = IBI                      

                if firstBeat :                        
                  firstBeat = 0                  
                  secondBeat = 1                  
                  continue                              

                runningTotal = 0
                for i in range(0,9):            
                  self.rate[i] = self.rate[i+1]       
                  runningTotal += self.rate[i]      

                self.rate[9] = IBI
                runningTotal += self.rate[9]        
                runningTotal /= 10
                BPM = 60000/runningTotal
                self.post_to_iot_hub(BPM)
                #print("BPM:" + str(BPM))
                # send_to_prcessing("B", BPM)
                # send_to_prcessing("Q", IBI)

          if Signal < th and Pulse == 1 :                    
              self.amp = P - T                   
              th = self.amp/2 + T
              T = th
              P = th
              Pulse = 0 
              
          if N > 2500 :
              th = 512
              T = th                  
              P = th                                              
              lastBeatTime = sampleCounter
              firstBeat = 0                     
              secondBeat = 0                   
              print("no beats found")

          time.sleep(0.005)