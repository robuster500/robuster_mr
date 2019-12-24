#!/usr/bin/env python3
import ctypes
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt32MultiArray
from std_msgs.msg import String
from std_msgs.msg import UInt16MultiArray
from std_msgs.msg import UInt8MultiArray
import sys, select, os,time
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

msg = """
Control Your robuster!
---------------------------
Moving around:
        h d l x 

h : open the dev heart
d : get dev ctlmode

l : open light lux

space key, x : force stop

CTRL-C to quit
"""
def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

'''
获取通过ros发送过来的小车控制指令
'''
def getdevStatus(statusData):
    # print(statusData)
    pass
    #revCmd = ctypes.c_int(ctlData.data[0]).value


'''
获取通过ros发送过来的小车控制指令
'''
def getdevError(statusData):
    pass
    # print(statusData)



def robuster_demo():
    global robuster_mode_pub    
    rospy.Subscriber("Dev_status", UInt32MultiArray, getdevStatus)
    rospy.Subscriber("Dev_error", UInt32MultiArray, getdevError)
    robuster_mode_pub = rospy.Publisher('DEV_CTL', UInt32MultiArray, queue_size=1000)
    rospy.init_node('robuster_sdk_demo', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    ctl_data = [1,1]
    ctl_send_data = UInt32MultiArray(data = ctl_data)
    robuster_mode_pub.publish(ctl_send_data)

    ctl_data = [2,0]
    ctl_send_data = UInt32MultiArray(data = ctl_data)
    robuster_mode_pub.publish(ctl_send_data)
    light_lux = 0
    while not rospy.is_shutdown():   
        key = getKey()
        if key == 'h':
            ctl_data = [1,1]
            ctl_send_data = UInt32MultiArray(data = ctl_data)
            robuster_mode_pub.publish(ctl_send_data)
            rospy.loginfo(ctl_send_data)
        if key == 'd':
            print("get dev ctl")
            ctl_data = [2,0]
            ctl_send_data = UInt32MultiArray(data = ctl_data)
            robuster_mode_pub.publish(ctl_send_data)            
            rospy.loginfo(ctl_send_data)
        if key == 'l':
            print("control light")
            light_lux = 5 - light_lux
            ctl_data = [4,light_lux,light_lux]
            ctl_send_data = UInt32MultiArray(data = ctl_data)
            robuster_mode_pub.publish(ctl_send_data)                            
            rospy.loginfo(ctl_send_data)
        if key == 'x' or key == ' ':
            print("stop dev")
            return
        if (key == '\x03'):
            return
        rate.sleep()


if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
    try:   
        print(msg)     
        robuster_mode_pub = ''
        robuster_demo()
    except:
        print("Communications Failed")
    finally:
        ctl_data = [1,0]
        ctl_send_data = UInt32MultiArray(data = ctl_data)
        robuster_mode_pub.publish(ctl_send_data)
        rospy.loginfo(ctl_send_data)
        ctl_data = [2,1]
        ctl_send_data = UInt32MultiArray(data = ctl_data)
        robuster_mode_pub.publish(ctl_send_data)
        rospy.loginfo(ctl_send_data)
        ctl_data = [4,0,0]
        ctl_send_data = UInt32MultiArray(data = ctl_data)
        robuster_mode_pub.publish(ctl_send_data)
        rospy.loginfo(ctl_send_data)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
