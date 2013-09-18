#coding=utf-8
__author__ = 'yann'

from RFID import Tag
tag=Tag(port='com3',baudrate=57600,timeout=1000)
#tag.start()
#tag.Write(Len=0x04,Adr=0x00,Cmd=0x01)
tag.sendCMD(Len=0x04,Adr=0x00,Cmd=0x01)
tag.start()
print tag.data
