#coding=utf-8
__author__ = 'Neo Yan'

import serial
import threading
import time
import Basic
from Queue import Queue

class Tag(serial.Serial,threading.Thread):
    def __init__(self,**sersetting):

        threading.Thread.__init__(self)
        serial.Serial.__init__(self)


        self.port=sersetting.get('port')
        self.timeout=sersetting.get('timeout')
        self.baudrate=sersetting.get('baudrate')

        self.hasData=True

        self.data=''


        self.Area={'Reserved':'0x00','EPC':'0x01','TID':'0x02','UserArea':'0x03'}
        self.CMD={'Readall':'0x01','Readone':'0x02','Write':'0x03','MakeEPCID':'0x04','Erase':'0x07'}

        self.open()


    def run(self):
        if self.isOpen():
           cmd=self.queue.get()
           if len(cmd)>0:
              self.Write(cmd)
              self.Read()
           else:
               pass
        else:
            raise Exception('Serial port is closed')

    def sendCMD(self,**CMD):
        self.queue=Queue()
        self.queue.put(CMD)


    def Read(self,**CMD):
        while self.hasData:
            #读串口数据
            time.sleep(1)
            if self.inWaiting()>0:
                self.data=self.read(self.inWaiting())
                if len(self.data)>0:
                    self.flushOutput()
                print self.data.encode('hex')
            else:
                continue

                
    def Write(self,CMD):
    #发送串口指令
        CCmd=Basic.spliceCMD(CMD)
        self.write(CCmd)
        self.flushInput()












