import serial,struct
import time

ser=serial.Serial()
ser.port='Com3'
ser.baudrate=57600
ser.timeout=1000

def CRC16(x):
    b = 0x8408
    a = 0xFFFF
    for byte in x:
        a = a^byte
        for i in range(8):
            last = a%2
            a = a>>1
            if last ==1: a = a^b
    aa = '0'*(6-len(hex(a)))+hex(a)[2:]
    ll,hh =int(aa[:2],16),int(aa[2:],16)
    return [hh,ll]

def CRC161(x):
    b = 0x8408
    a = 0xFFFF
    for byte in x:
        a = a^byte
        for i in range(8):
            last = a%2
            a = a>>1
            if last ==1: a = a^b
    aa = '0'*(6-len(hex(a)))+hex(a)[2:]
    ll,hh =aa[:2],aa[2:]
    return [hh,ll]


CMD=lambda x:struct.pack('B',x)

Len=0x04
Adr=0x00
Code=0x01
Data1=0x00
Data2=0x00

CRC16_TMP1=CRC16([Len,Adr,Code])
#CRC16_TMP=CRC16([Len,Adr,Code,Data1,Data2])
CRC16_values=[struct.pack('B',k) for k in CRC16_TMP1]

CMD1=CMD(Len)+CMD(Adr)+CMD(Code)+CRC16_values[0]+CRC16_values[1]

if ser.isOpen():
    ser.close()
ser.open()
ser.write(CMD1)

time.sleep(5)
n=ser.read(ser.inWaiting())
print n.encode('hex')