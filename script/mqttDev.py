#!/usr/bin/env python3
#-*-coding:utf-8-*-

# 导入 paho-mqtt 的 Client：
#import paho.mqtt.client as mqtt
import time
import Robuster
import operator
import ctypes
from std_msgs.msg import UInt32MultiArray
import robusterRos
from cmdCombineOpt import cmdCombineOpt as cmbopt
import struct
import json
import subprocess
import signal
import os
import re

unacked_sub = [] #未获得服务器响应的订阅消息 id 列表
sg_heartStatus = 0
sg_devStatus = 1
sg_deviceCtl = 1
devCmdOpt = ''


deviceId = "11111111111111111"
DataPusherTopic = "/Data"
errorPusherTopic = "/error"
replyPusherTopic = "/reply"
connectSubscriber = "/connect"
cmdSubscriber = "/cmd"


def DevCmdOpt(cmd,parm):
    global devCmdOpt,sg_deviceCtl
    try:
        if cmd == 0x01:   
            forSpeed = parm[0] << 8 | parm[1]
            bakSpeed = parm[2] << 8 | parm[3]
            print(forSpeed,bakSpeed)
            setSpeedValue(forSpeed,bakSpeed)    
        if cmd == 0x03:
            forLux = parm[0]
            bakLux = parm[1]
            devCmdOpt.sendLightCmd(forLux,bakLux)
        if cmd == 0x04:
            waining = parm[0]
            devCmdOpt.sendReWarningCmd(warning)
        if cmd == 0x05:
            ctlStatus = parm[0]
            print(ctlStatus)
            sg_deviceCtl = 1 - ctlStatus
            devCmdOpt.sendCtlCmd(ctlStatus)
        publishData(deviceId + replyPusherTopic,str(cmd) + '1')            
    except:
        publishData(deviceId + replyPusherTopic,str(cmd) + '0')
    

def ansyRemoteCtlCmd(topic,data):   
    global sg_devStatus
    try:
        print(data)
        # print(type(data))
        # cmd = int(chr(data[0]))
        cmd = data[0]
        if operator.eq(topic,deviceId + connectSubscriber) == True: 
            print("connect %d" % cmd)
            if cmd == 0:
                sg_devStatus = 1
            else:
                sg_devStatus = 0
        if sg_devStatus == 0:
            return
        if operator.eq(topic,deviceId + cmdSubscriber) == True:       
            parm = data[1:]
            DevCmdOpt(cmd,parm)
    except:
        publishData(deviceId + replyPusherTopic,data[0] + '0')


# 用于响应服务器端 CONNACK 的 callback，如果连接正常建立，rc 值为 0
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))

# 用于响应服务器端 PUBLISH 消息的 callback，打印消息主题和内容
def on_message(client, userdata, msg):     
    ansyRemoteCtlCmd(msg.topic,msg.payload)

# 在连接断开时的 callback，打印 result code
def on_disconnect(client, userdata, rc):
    global sg_devStatus,sg_heartStatus
    print("Disconnection returned result:"+ str(rc))
    #sg_heartStatus = 0
    #sg_devStatus = 1

# 在订阅获得服务器响应后，从为响应列表中删除该消息 id
def on_subscribe(client, userdata, mid, granted_qos):
    unacked_sub.remove(mid)

MqttDev = ''
def createClient(ip):
    global MqttDev
    # 构造一个 Client 实例
    MqttDev = mqtt.Client()

    MqttDev.on_connect = on_connect

    MqttDev.on_disconnect= on_disconnect

    MqttDev.on_message = on_message

    MqttDev.on_subscribe = on_subscribe
    # 连接 broker
    # connect() 函数是阻塞的，在连接成功或失败后返回。如果想使用异步非阻塞方式，可以使用 connect_async() 函数。
    MqttDev.connect(ip, 1883, 60)
    MqttDev.loop_start()

def subscribeTopic(topic):
  #  global MqttDev
    # 订阅单个主题
   # result, mid = MqttDev.subscribe(topic, 0)
    #print ("result %d" %result)
    #unacked_sub.append(mid)
    pass

def disconnMqtt():
    global MqttDev,sg_devStatus
    # 断开连接
    MqttDev.loop_stop()
    MqttDev.disconnect()
    sg_devStatus = 0

def publishData(topic,data):
    pass
    

def HeartConnect(HeartCount):
    global sg_heartStatus,devCmdOpt
    if HeartCount % 20 == 0:        
        devCmdOpt.sendHeartData(sg_heartStatus)

def wheelSpeedCallBack(speedData):
    global devCmdOpt
    
    lspeed = ctypes.c_int(speedData.data[0]).value
    rspeed = ctypes.c_int(speedData.data[1]).value    
    setSpeedValue(lspeed,rspeed)
    # set speed to dev 
    print("%d,%d" %(lspeed,rspeed))
    devCmdOpt.sendPidCmd(lspeed,rspeed,5)
'''
获取RTK数据
'''
def rtkCallBack(gpsData):
    global MqttDev,devCmdOpt,sg_devStatus,deviceId,connectSubscriber,cmdSubscriber,DataPusherTopic,errorPusherTopic
    try:
        jsonData = {}
        gpsdataList = []
        temp = struct.pack('f',gpsData.latitude)
        gpsdataList += list(temp)
    
        temp = struct.pack('f',gpsData.longitude)
        gpsdataList += list(temp)
        
        temp = struct.pack('f',gpsData.altitude)
        gpsdataList += list(temp)
        
        temp = struct.pack('i',gpsData.status.status)        
        gpsdataList += list(temp)[0:1]    
    
        jsonData = {"data":gpsdataList}
        jsonData["funcode"] = [0xA4,0x04]
        publishData(deviceId + DataPusherTopic, json.dumps(jsonData))
    except:
        print("gps data analy error")

DEV_HRART       = 0x01
DEV_CTL         = 0x02
DEV_WARNING     = 0x03
DEV_LUX         = 0x04
DEV_DEVICEID    = 0x05
DEV_SETIP       = 0x06
DEV_POWERSW     = 0x07
DEV_ULTRASW     = 0x08

'''
获取通过ros发送过来的小车控制指令
'''
def getCtlCmdforRos(ctlData):
    global MqttDev,devCmdOpt,sg_devStatus,deviceId
    revCmd = ctypes.c_int(ctlData.data[0]).value
    if(revCmd == DEV_HRART):
        sg_devStatus = ctypes.c_int(ctlData.data[1]).value
    if(revCmd == DEV_CTL):
        ctlcmd = ctypes.c_int(ctlData.data[1]).value
        devCmdOpt.sendCtlCmd(ctlcmd)
    if(revCmd == DEV_WARNING):
        warningStatus = ctypes.c_int(ctlData.data[1]).value
        devCmdOpt.sendReWarningCmd(warningStatus)
    if(revCmd == DEV_LUX):
        forLux = ctypes.c_int(ctlData.data[1]).value
        bakLux = ctypes.c_int(ctlData.data[2]).value
        devCmdOpt.sendLightCmd(forLux,bakLux)
    if(revCmd == DEV_DEVICEID):
        # send device id to ros
        robusterRos.publishDevice(deviceId)
    if(revCmd == DEV_SETIP):    
        ip = ctypes.c_int(ctlData.data[1]).value
        port = ctypes.c_int(ctlData.data[2]).value
        devCmdOpt.sendIPInfoDataCmd(ip,port)
    if(revCmd == DEV_POWERSW):
        outputSw = ctypes.c_int(ctlData.data[1]).value        
        devSw = ctypes.c_int(ctlData.data[2]).value        
        devCmdOpt.sendPowerDataCmd(outputSw,devSw)
    if(revCmd == DEV_ULTRASW):
        ultraSw = ctypes.c_int(ctlData.data[1]).value
        devCmdOpt.sendUltraSWDataCmd(ultraSw)
'''
获取设备的id号，用于做发布和监听区分
'''
def getDeviceId():
    global MqttDev,devCmdOpt,sg_devStatus,deviceId,connectSubscriber,cmdSubscriber,DataPusherTopic,errorPusherTopic
    #get dev ctl power    
    HeartConnect(0)
    devCmdOpt.sendCtlCmd(0)
    time.sleep(0.01)
    countTime = 0
    while True:        
        devCmdOpt.sendDevInfoDataCmd()
        time.sleep(0.1)
        Robuster.RobusterLoop()
        jsonData =  Robuster.RobusterRead()
        if jsonData != [] and jsonData != None:
            for devjsonData in jsonData: 
                if operator.eq(devjsonData['funcode'],cmbopt.DEV_NUM_INFO_CMD) == True:                    
                    deviceId = "".join([chr(x) for x in devjsonData['data'][:17]])
                    print("deviceID:" + deviceId)
                    devCmdOpt.sendCtlCmd(1)
                    return True
        countTime += 1
        if countTime > 30:
            return False


            
g_forSpeed = 0
g_bakSpeed = 0
g_speedCount = 0

def setSpeedValue(forspeed,bakspeed):
    global g_forSpeed,g_bakSpeed
    g_forSpeed = forspeed
    g_bakSpeed = bakspeed
                                    
def sendSpeedLoop():
    global devCmdOpt,g_forSpeed,g_bakSpeed,g_speedCount,sg_deviceCtl
    # 10ms
    g_speedCount += 1
    if g_speedCount % 5 == 0 and sg_deviceCtl == 1:
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
    global MqttDev,devCmdOpt,sg_devStatus,deviceId,connectSubscriber,cmdSubscriber,DataPusherTopic,errorPusherTopic
    signal.signal(signal.SIGINT,exitFunc)
    signal.signal(signal.SIGTERM,exitFunc)
    HeartCount = 0
    ip = "192.168.1.196"
    port = 9999
    if ConnectDev(ip,port) == False:        
        return 0
    #获取下发数据对象
    devCmdOpt = Robuster.getDevCmdOpt()
    #获取设备ID
    if getDeviceId() == False:
        return
    # 连接云服务器 emq
   # createClient("120.78.81.39")
    #mqtt监听端口
    subscribeTopic(deviceId + connectSubscriber)
    subscribeTopic(deviceId + cmdSubscriber)
    # init ros node
    robusterRos.initRosTalker(wheelSpeedCallBack,rtkCallBack,getCtlCmdforRos)    
    while True:
        if Robuster.RobusterCheckLink() == 0:
            sg_devStatus = 0
            ConnectDev(ip,port)
            # 断开连接
            timeOutCmd = {"funcode":[0xA2,0x05]}
            publishData(deviceId + errorPusherTopic, json.dumps(timeOutCmd))
        else:
            #不停的发送速度信息
            sendSpeedLoop()        
        if sg_devStatus == 1:
            # 循环timeout机制
            timeOutCmd = []
            try:
                timeOutCmd = Robuster.RobusterLoop()
                if timeOutCmd != [] and timeOutCmd != None:
                    publishData(deviceId + errorPusherTopic,json.dumps(timeOutCmd))
                    robusterRos.publishError(timeOutCmd)
            except:
                print("ansy error: %s" %timeOutCmd)

            # 获取设备数据 json格式            
            jsonData =  Robuster.RobusterRead()                 
            if jsonData != [] and jsonData != None:                      
                publishData(deviceId + DataPusherTopic,json.dumps(jsonData))  
                for devjsonData in jsonData:   
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_DECODE_CMD) == True:
                        # 发布decode里程数据
                        robusterRos.publishDecode(devjsonData['data'])
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_IMU_CMD) == True:
                        # 发布imu 数据到ros节点
                        robusterRos.publishImu(devjsonData['data'])
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_CSB_CMD) == True:
                        # 发布csb数据
                        robusterRos.publishCSB(devjsonData['data'])                   
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_DEV_STATUS_CMD) == True:
                        # 发布status数据
                        robusterRos.publishStatus(devjsonData['data'])                                                
                    # 自动获取控制权限。
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_DEV_STATUS_CMD) == True:
                        if devjsonData['data'][1] != 0x02:
                            devCmdOpt.sendCtlCmd(0)              
                    if operator.eq(devjsonData['funcode'],cmbopt.DEV_SET_POWER_CMD) == True:
                        print("had halt")
                        exit("exit code for ctrl + C")                        
                        subprocess.call("echo '123466' | sudo -S shutdown -r now",shell = True)
                        #halt system
            time.sleep(0.01)
            HeartCount += 1
            HeartConnect(HeartCount)
        else:
            time.sleep(0.01)
if __name__ == '__main__':
    main()
