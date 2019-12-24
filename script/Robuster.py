#-*-coding:utf-8-*-
import operator
from cmdCombineOpt import cmdCombineOpt as cmbopt
from ansyData import ansyDevData as ansyDataForDev
import time
import RobusterTimeOut
from RobustertcpClient import RobusterClient as client
devSerial = ''
devCmbopt = ''
ansyDD = ansyDataForDev()

def initRobuster(ip,port):
    global devSerial,devCmbopt
    try:
        try:
            devSerial = client(ip,port)    
        except:
            print("tcp server connect false")    
        devCmbopt = cmbopt(devSerial)    
        RobusterTimeOut.initRobusterTime(devSerial)   
        devCmbopt.sendHeartData(0)  
        time.sleep(0.1)     
        jsonData = RobusterRead()
        if jsonData != [] and jsonData != None:
            return True 
    except:
        print("tcp server open false")
        return 0

def RobusterCheckLink():
    global devSerial
    return devSerial.checkClient()

def RobusterLoop():
    global devCmbopt,devSerial
    rpyCmd = RobusterTimeOut.RobusterLoop()
    return rpyCmd

revBuffFIfo = []

def RobusterRead():
    global devCmbopt,devSerial,ansyDD,revBuffFIfo        
    while True:
        revdata,revLen = devSerial.readOpt()
        if revLen != 0:
            #set data to fifo
            revBuffFIfo += (revdata)
            continue
        elif len(revBuffFIfo) > 0:
            #ansy rev data        
            # dict  'data' 'funcode'        
            revjsonCmd,readlen = ansyDD.AnsyDataDev(revBuffFIfo)
            # print json
            if readlen == 0:
                revBuffFIfo = []
            else:
                revBuffFIfo = revBuffFIfo[-readlen -1:]
                
            setTimeOutCmd(revjsonCmd)
            return revjsonCmd
        else:
            return []
def setTimeOutCmd(revjsonCmd):
    global cmbopt
    for jsonData in revjsonCmd:
        if operator.eq(jsonData['funcode'],cmbopt.DEV_REPLAY_CMD) == True:       
            RobusterTimeOut.setWatiCmd(jsonData['data'][:2])
        elif operator.eq(jsonData['funcode'],cmbopt.DEV_HEART_CMD) == True:
            RobusterTimeOut.setWatiCmd(cmbopt.ROBOT_HEART_CMD)
        else:
            RobusterTimeOut.setWatiCmd(jsonData['funcode'])
def getDevCmdOpt():
    global devCmbopt
    if devCmbopt != '':
        return devCmbopt
    else:
        return ''

def closeClient():
    global devSerial
    devSerial.closeClient()












