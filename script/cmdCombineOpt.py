#-*-coding:utf-8-*-
import os
import sys
import RobusterTimeOut

class cmdCombineOpt:
    g_oriSendbuff = [0xf4,0xF5,0x00,0x00,0x00,0x00]

    # robot to dev
    ROBOT_HEART_CMD = [0x01,0x01]
    ROBOT_GET_CTL_CMD = [0x01,0x02]
    ROBOT_RELEASE_WARNING_CMD = [0x01,0x03]
    ROBOT_NOPID_CTL_CMD = [0x02,0x01]
    ROBOT_PID_CTL_CMD = [0x02,0x02]
    ROBOT_LIGHT_CMD = [0x02,0x03]
    ROBOT_PARKCAT_CMD = [0x02,0x04]
    ROBOT_REPLAY_DATA_CMD = [0x02,0x05]
    ROBOT_DEV_INFO_CMD = [0x02,0x06]
    ROBOT_IP_INFO_CMD =  [0x02,0x07]
    ROBOT_DEV_POWER_CMD = [0x02,0x08]
    ROBOT_TIME_OUT_CMD = [0x02,0x09]
    ROBOT_WORK_MODE_CMD = [0x02,0x0A]          
    ROBOT_ULTRA_SW_CMD = [0x02,0x0B]    

    #dev to robot
    DEV_DEV_STATUS_CMD = [0xA0,0x01]
    DEV_REQUEST_CMD = [0xA0,0x02]
    DEV_HEART_CMD = [0xA0,0x03]
    DEV_REPLAY_CMD = [0xA0,0x04]
    DEV_NUM_INFO_CMD = [0xA0,0x05]
    DEV_SET_POWER_CMD = [0xA0,0x06]

    #dev push to robot
    DEV_IMU_CMD = [0xA1,0x01]
    DEV_DECODE_CMD = [0xA1,0x02]
    DEV_CSB_CMD = [0xA1,0x03]

    g_sendbuff = []
    sendDataFunc = ''
    def __init__(self,funcSendData):
        self.sendDataFunc = funcSendData      

    def crc16(self,x, invert):
        a = 0xFFFF
        b = 0xA001
        for byte in x:
            a ^= byte
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        return ((a & 0xFF00) >> 8 ),(a & 0x00FF)

    def calcCrc16(self,sendbuff,rever = True):
        crc = []
        crcH,crcL = self.crc16(sendbuff,rever)
        if rever == True:
            crc.append(crcH)
            crc.append(crcL)
        else:
            crc.append(crcL)
            crc.append(crcH)            
        return crc

    def sendHeartData(self,status):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_HEART_CMD
        self.g_sendbuff.append(1)
        self.g_sendbuff.append(status)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])
        tmp_sendbuff = self.g_sendbuff        
        self.g_sendbuff = []        
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_HEART_CMD

        RobusterTimeOut.intoWaitCmd(cmd)
        return tmp_sendbuff

    def sendCtlCmd(self,status):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_GET_CTL_CMD
        self.g_sendbuff.append(1)
        self.g_sendbuff.append(status)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_GET_CTL_CMD

        RobusterTimeOut.intoWaitCmd(cmd)
        return tmp_sendbuff
        
    def sendReWarningCmd(self,warning):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_RELEASE_WARNING_CMD
        self.g_sendbuff.append(1)
        self.g_sendbuff.append(warning)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_RELEASE_WARNING_CMD

        RobusterTimeOut.intoWaitCmd(cmd)        
        return tmp_sendbuff

    def sendNoPidCmd(self,forSpeed,bakSpeed,runmode):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_NOPID_CTL_CMD

        self.g_sendbuff.append(5)        
        self.g_sendbuff.append(runmode)
        self.g_sendbuff += [((forSpeed & 0xFF00) >> 8),(forSpeed & 0x00FF)]
        self.g_sendbuff += [((bakSpeed & 0xFF00) >> 8),(bakSpeed & 0x00FF)]

        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)
        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_NOPID_CTL_CMD

        #RobusterTimeOut.intoWaitCmd(cmd)    
        return tmp_sendbuff
    def sendPidCmd(self,forSpeed,bakSpeed,runmode):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_PID_CTL_CMD

        self.g_sendbuff.append(5)        
        self.g_sendbuff.append(runmode)
        self.g_sendbuff += [((forSpeed & 0xFF00) >> 8),(forSpeed & 0x00FF)]
        self.g_sendbuff += [((bakSpeed & 0xFF00) >> 8),(bakSpeed & 0x00FF)]

        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_PID_CTL_CMD

        #RobusterTimeOut.intoWaitCmd(cmd) 
        return tmp_sendbuff

    def sendLightCmd(self,forlum,baklum):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_LIGHT_CMD

        self.g_sendbuff.append(2)
        self.g_sendbuff.append(forlum)
        self.g_sendbuff.append(baklum)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)
        
        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_LIGHT_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff
    def sendParkCatCmd(self,status):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_PARKCAT_CMD

        self.g_sendbuff.append(1)
        self.g_sendbuff.append(status)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_PARKCAT_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendReplayDataCmd(self,status):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_REPLAY_DATA_CMD

        self.g_sendbuff.append(1)
        self.g_sendbuff.append(status)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_REPLAY_DATA_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendDevInfoDataCmd(self):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_DEV_INFO_CMD

        self.g_sendbuff.append(0)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_DEV_INFO_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendIPInfoDataCmd(self,ipaddress,port):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_IP_INFO_CMD

        self.g_sendbuff.append(6)
        self.g_sendbuff.append(((ipaddress & 0xFF000000) >> 24),((ipaddress & 0x00FF0000) >> 16),((ipaddress & 0x0000FF00) >> 8),(ipaddress & 0x000000FF))
        self.g_sendbuff.append(((port & 0xFF00) >> 8),(port & 0x00FF))
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_IP_INFO_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendPowerDataCmd(self,output,devPower):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_DEV_POWER_CMD

        self.g_sendbuff.append(2)       
        self.g_sendbuff.append(output) 
        self.g_sendbuff.append(devPower)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_DEV_POWER_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendTimeOutDataCmd(self,timeout):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_TIME_OUT_CMD

        self.g_sendbuff.append(1)       
        self.g_sendbuff.append(timeout)         
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_TIME_OUT_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff

    def sendWorkModeDataCmd(self,workMode):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_WORK_MODE_CMD

        self.g_sendbuff.append(1)       
        self.g_sendbuff.append(workMode)         
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_WORK_MODE_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff   

    def sendUltraSWDataCmd(self,sw):
        tmp_sendbuff = []
        self.g_sendbuff += self.g_oriSendbuff
        self.g_sendbuff += self.ROBOT_ULTRA_SW_CMD

        self.g_sendbuff.append(1)
        self.g_sendbuff.append(sw)
        self.g_sendbuff += self.calcCrc16(self.g_sendbuff[2:])

        tmp_sendbuff =  self.g_sendbuff        
        self.g_sendbuff = []
        self.sendDataFunc.writeOpt(tmp_sendbuff)

        cmd = {}
        cmd['sendbuff'] = tmp_sendbuff
        cmd['replay'] = 3
        cmd['cmdbuff'] = self.ROBOT_ULTRA_SW_CMD

        RobusterTimeOut.intoWaitCmd(cmd)         
        return tmp_sendbuff       
