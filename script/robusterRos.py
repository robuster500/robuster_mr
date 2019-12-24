#!/usr/bin/env python3
# license removed for brevity
import ctypes
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt32MultiArray
from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
decodePub = ''
imuPub = ''
csbPub = ''
errorPub = ''
statusPub = ''
deviceIDPub = ''
rate = 0

def initRosTalker(wheelSpeedCallBack,rtkCallBack,getCtlCmdforRos):
    global decodePub,imuPub,rate,csbPub,errorPub,statusPub,deviceIDPub
    decodePub = rospy.Publisher('Dev_decode', UInt32MultiArray, queue_size=1000)
    imuPub = rospy.Publisher('Dev_imu', UInt32MultiArray, queue_size=1000)
    csbPub = rospy.Publisher('Dev_csb', UInt32MultiArray, queue_size=1000)
    errorPub = rospy.Publisher('Dev_error', UInt32MultiArray, queue_size=1000)
    statusPub = rospy.Publisher('Dev_status', UInt8MultiArray, queue_size=1000)
    deviceIDPub = rospy.Publisher('Dev_deviceID', String, queue_size=1000)

    rospy.Subscriber("WheelSpeed", UInt32MultiArray, wheelSpeedCallBack)    
    rospy.Subscriber("GPS_RTK", NavSatFix, rtkCallBack)
    rospy.Subscriber("DEV_CTL", UInt32MultiArray, getCtlCmdforRos)
    rospy.init_node('robuster_Dev', anonymous=True)
    rate = rospy.Rate(20) # 10hz


def publishCSB(csbData):
    global csbPub
    csbNum = []
    csbNum.append(csbData[0:2])
    csbNum.append(csbData[2:4])
    csbNum.append(csbData[4:6])
    csbNum.append(csbData[6:8])
    csb_int16 = []
    csb_int16.append(int.from_bytes(csbNum[0],byteorder = "little"))
    csb_int16.append(int.from_bytes(csbNum[1],byteorder = "little"))
    csb_int16.append(int.from_bytes(csbNum[2],byteorder = "little"))
    csb_int16.append(int.from_bytes(csbNum[3],byteorder = "little"))
    left_top = UInt32MultiArray(data = csb_int16)
    csbPub.publish(left_top)

def publishError(errData):
    global errorPub
    errNum = []
    errNum.append(errData[4:6])    
    error_int16 = []
    error_int16.append(int.from_bytes(errNum[0],byteorder = "little"))    
    left_top = UInt32MultiArray(data = error_int16)
    errorPub.publish(left_top)

def publishStatus(statusData):
    global statusPub    
    left_top = UInt8MultiArray(data = statusData[0:5])
    statusPub.publish(left_top)

def publishDevice(deviceID):
    global deviceIDPub    
    left_top = String(data = deviceID)
    deviceIDPub.publish(left_top)


def publishDecode(decode):
    global decodePub
    decodeNum = []
    decodeNum.append(decode[0:4])
    decodeNum.append(decode[4:8])
    decodeNum.append(decode[8:12])
    decodeNum.append(decode[12:16])

    decode_int32 = []
    decode_int32.append(int.from_bytes(decodeNum[0],byteorder = "little"))
    decode_int32.append(int.from_bytes(decodeNum[1],byteorder = "little"))
    decode_int32.append(int.from_bytes(decodeNum[2],byteorder = "little"))
    decode_int32.append(int.from_bytes(decodeNum[3],byteorder = "little"))
    left_top = UInt32MultiArray(data = decode_int32)    
    decodePub.publish(left_top)
    # rospy.loginfo(left_top)    

def publishImu(imu):  
    global imuPub
    imuNum = []
    imuNum.append(imu[0:4]) 
    imuNum.append(imu[4:8]) 
    imu_int32 = []
    imu_int32.append(int.from_bytes(imuNum[0],byteorder = "little"))    
    imu_int32.append(int.from_bytes(imuNum[1],byteorder = "little"))
    left_top = UInt32MultiArray(data = imu_int32)    
    imuPub.publish(left_top)
    # rospy.loginfo(left_top)    

# def talker():
#     pub = rospy.Publisher('chatter', Int32MultiArray, queue_size=300)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     hello_int = [33,36]
#     left_top = Int32MultiArray(data = hello_int)
#     while not rospy.is_shutdown():
#         # = "hello world %s" % rospy.get_time()
#         rospy.loginfo(left_top)
#         pub.publish(left_top)
#         rate.sleep()



# if __name__ == '__main__':
#     try:
#         talker()
#     except rospy.ROSInterruptException:
#         pass
