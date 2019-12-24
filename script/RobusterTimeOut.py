#!/usr/bin/env python3
#-*-coding:utf-8-*-

import time
import operator
sendCmdList = []
sendBuffFunc = ''
def nowTime():
    t = int(time.time()*1000)
    return t

def initRobusterTime(funcSendbuff):
    global sendBuffFunc
    sendBuffFunc = funcSendbuff

def RobusterLoop():
    return foreachCmd()    

def foreachCmd():
    global sendCmdList
    listData = []
    for cmd in sendCmdList:
        if nowTime() - cmd['timeout'] > 100:  
            data = replayData(cmd)
            sendCmdList.remove(cmd)                
            if data['replay'] == 0:
                listData.append(data)
            else:
                sendCmdList.append(data)
    return listData

#cmdData dict   "timeout","sendbuff","cmdbuff","replay"
def intoWaitCmd(cmdData):
    global sendCmdList , nowTime
    cmdData['timeout'] = nowTime()
    sendCmdList.append(cmdData)


def setWatiCmd(cmd):
    global sendCmdList
    for data in sendCmdList:
        if operator.eq(data['cmdbuff'],cmd) == True:
            sendCmdList.remove(data)

def replayData(cmd):
    global nowTime,sendBuffFunc
    if cmd['replay'] == 0:
        return cmd
    else:
        sendBuffFunc.writeOpt(cmd['sendbuff'])
        cmd['timeout'] = nowTime()
        cmd['replay'] -= 1        
    return cmd


































