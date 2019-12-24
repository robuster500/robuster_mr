#-*-coding:utf-8-*-

import re
import operator
from cmdCombineOpt import cmdCombineOpt as ccbo

class ansyDevData:

    combine = ccbo("") 
    def __init__(self):
        pass

    def AnsyDataDev(self,revBuff):
        global combine
        curstatus = 0
        listjson = []
        intlist = []
        readLen = 0
        
        for orddata in revBuff:        
            intlist.append(orddata)    
                    
        oriDataList = []        
        proData = 0
        beiginFlag = 0  
        readList = []    
        readListLen = 0
        for data in intlist:
            if curstatus == 0:             
                if(data == 0xF5 and proData == 0xF4):
                    curstatus = 1
                    continue
                proData = data
            elif curstatus == 1:
                oriDataList.append(data)
                if len(oriDataList) == 7:
                    readListLen = oriDataList[6]
                if len(oriDataList) == readListLen + 9:
                    crc = self.combine.calcCrc16(oriDataList[:-2],False)                    
                 
                    if(operator.eq(crc,oriDataList[-2:]) == True):                    
                        readList.append(oriDataList)                                     
                    oriDataList = []
                    curstatus = 0
                    
        for data in readList:                        
            if len(data) > 1:
                jsonData , ansyStatus = self.getDecode(data)       
                if ansyStatus == True:
                    listjson.append(jsonData)        
                else:
                    readLen = (len(data) + 1)
                    break                  
                continue      
        return listjson,readLen

    def getDecode(self,intlist):
        replay = False
        listJosn = {}
        cmd = intlist[4:6]        
        datalen = intlist[6]
        if(operator.eq(cmd,ccbo.DEV_HEART_CMD) == True):            
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_DECODE_CMD) == True):                        
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_IMU_CMD) == True):                            
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_REPLAY_CMD) == True):                         
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_DEV_STATUS_CMD) == True):                        
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_SET_POWER_CMD) == True):                
            replay = True            
        elif(operator.eq(cmd,ccbo.DEV_CSB_CMD) == True):                           
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_REQUEST_CMD) == True):                                      
            replay = True
        elif(operator.eq(cmd,ccbo.DEV_NUM_INFO_CMD) == True):                                               
            replay = True            
        
        listJosn = {"data":intlist[7:datalen + 7]}             
        listJosn["funcode"] = cmd       
        return listJosn,replay
        

