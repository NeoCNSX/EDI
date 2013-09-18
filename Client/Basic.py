#coding=utf-8

__author__ = 'Neo Yan'

import struct

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
    hh,ll=int(aa[2:],16),int(aa[:2],16)
    return [hh,ll]


def spliceCMD(CMD):
    if isinstance(CMD,dict):
        try:
            Len=CMD['Len']
            Adr=CMD['Adr']
            Cmd=CMD['Cmd']
            Data=CMD.get('Data')

            CMDList=[Len,Adr,Cmd]

            if Data is not None:
                if isinstance(Data,list):
                    CMDList+=Data
                else:
                    raise Exception('Need List type')
            else:
                pass

            return make2CCMD(CMDList)
        except KeyError :
            raise Exception('Cannot find key and value')
    else:
        raise Exception('Need Dict type')






def make2CCMD(cmditems):
    if not isinstance(cmditems,list):
       raise Exception('Need List type')
    else:
        py2c=lambda x:struct.pack('B',x) #包装成C无符号整型
        CRC16values=CRC16(cmditems)       #计算CRC16值，高字节在前，低字节在后
        cmditems.extend(CRC16values)      #组成完整的命令序列
        CMDlist=map(py2c,cmditems)        #包装命令序列
        CMD=''.join(each for each in CMDlist)  #出于读写串口需要，组成命令字符串
        return CMD

def getData(data,lenindex=0,beginindex=4,lencmd=5,cutchar='\x0D',ismultiple=True):
    '''
       data:从串口获取到的数据
       lenindex:data字段长度字节的索引
       lencmd:命令和CRC16的长度，默认占5个字节不包括Len字段
       beginindex:数据字段的起始索引
       cutchar:用于切割多个标签的字符
       ismultiple:获取多条数据和单条数据的布尔值
    '''
    datalen=ord(data[lenindex])-lencmd
    #dataend=beginindex+datalen
    #alldata=data[lencmd:dataend]

    #if ismultiple:
        #totalTAG=ord(data[lencmd-1])
        #beginindex+=1
        #alldata=alldata.split(cutchar)
    beginindex+=1 if ismultiple else beginindex

    endindex=beginindex+datalen

    alldata=data[beginindex:endindex]

    alldata=alldata.split(cutchar) if ismultiple else alldata

    return alldata



def getByte(data,byteindex):
    if not isinstance(data,list):
        raise Exception('Need List type')
    else:
        return data[byteindex]


