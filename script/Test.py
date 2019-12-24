#!/usr/bin python3
#-*-coding:utf-8-*-

import time
import Robuster
import operator
from cmdCombineOpt import cmdCombineOpt as cmbopt
import struct
import subprocess
import signal
import os
import re
devCmdOpt = ""
sg_heartStatus = 0
def HeartConnect(HeartCount):
    global sg_heartStatus,devCmdOpt
    if HeartCount % 30 == 0:        
        devCmdOpt.sendHeartData(sg_heartStatus)

'''
获取设备的id号，用于做发布和监听区分
'''
def getDeviceId():
    global devCmdOpt,deviceId
    #get dev ctl power    
    HeartConnect(0)
    devCmdOpt.sendCtlCmd(0)
    time.sleep(0.01)
    countTime = 0
    while True:        
        devCmdOpt.sendDevInfoDataCmd()
        time.sleep(0.1)
        timeOutCmd = Robuster.RobusterLoop()
        jsonData =  Robuster.RobusterRead()
        if jsonData != [] and jsonData != None:
            for devjsonData in jsonData: 
                if operator.eq(devjsonData['funcode'],cmbopt.DEV_NUM_INFO_CMD) == True:
                    deviceId = "".join([chr(x) for x in devjsonData['data'][:17]])
                    print("deviceID:" + str(deviceId))
                    #devCmdOpt.sendCtlCmd(1)
                    return True
        countTime += 1
        if countTime > 300:
            return False


g_forSpeed = 100
g_bakSpeed = 100
g_speedCount = 0
def setSpeedValue(forspeed,bakspeed):
    global g_forSpeed,g_bakSpeed
    g_forSpeed = forspeed
    g_bakSpeed = bakspeed
                                    
def sendSpeedLoop():
    global devCmdOpt,g_forSpeed,g_bakSpeed,g_speedCount
    # 10ms
    g_speedCount += 1
    if g_speedCount % 10 == 0:
        g_speedCount = 0
        devCmdOpt.sendPidCmd(g_forSpeed,g_bakSpeed,5)   


def ConnectDev(ip,port):
    if Robuster.initRobuster(ip,port) == False:
        print("dev connect false")
        return False
    else:
        print("dev connect success")
        return True

def exitFunc(args,argv):
    Robuster.closeClient()
    print("exit")    
    os._exit(0)

def main():
    global devCmdOpt
    signal.signal(signal.SIGINT,exitFunc)
    signal.signal(signal.SIGTERM,exitFunc)

    ip = "192.168.1.196"
    port = 9999
    if ConnectDev(ip,port) == False:
        print("connect false")
        return 0
    #获取下发数据对象
    devCmdOpt = Robuster.getDevCmdOpt()
    #获取设备ID
    if getDeviceId() == False:
        return
    HeartCount = 0    
    while True:
        #check tcp link status
        if Robuster.RobusterCheckLink() == 0:
            ConnectDev(ip,port)
            time.sleep(0.01)
        else:
            #不停的发送速度信息
            sendSpeedLoop()
            # 循环timeout机制
            timeOutCmd = []
            try:
                timeOutCmd = Robuster.RobusterLoop()                
                if timeOutCmd != []:
                    print(timeOutCmd)    
            except:
                print("ansy error: %s" %timeOutCmd)
            # 获取设备数据 json格式            
            jsonData =  Robuster.RobusterRead()        
            time.sleep(0.01)
            HeartCount += 1
            HeartConnect(HeartCount)
if __name__ == '__main__':
    main()
