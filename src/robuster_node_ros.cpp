#include "ros/ros.h"
#include "std_msgs/String.h"
#include <geometry_msgs/Twist.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include "tf/transform_datatypes.h"
#include "robuster_node_ros.h"
#include "robuster_node_mile.h"

void initNodeRos(ros::Publisher &odom_pub,ros::NodeHandle n)
{    
	//定义消息发布者来发布“odom”消息
	odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
}

int loopNodeRos()
{
    ros::spinOnce();
    int a =1;
    int b = 0;
    if(ros::ok())
    {
        return a;
    }
    else
    {
        return b;
    }
}


//你自己填充
void pushMailData(ros::Publisher odom_pub,tf::TransformBroadcaster odom_broadcaster,double pose_theta,double x, double y, double vx, double vy, double vth)
{
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(pose_theta);
    geometry_msgs::TransformStamped odom_trans;
	ros::Time begin = ros::Time::now();
    odom_trans.header.stamp = begin;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";
    
    //用来自里程计的数据填充transform消息，并稍后用TransformBroadcaster发送出去，
    odom_trans.transform.translation.x = x;
    odom_trans.transform.translation.y = y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);



    //我们还要发布nav_msgs/Odometry消息，让导航包获取机器人的速度。创建消息变量，然后填充时间戳。(发布nav_msgs/Odometry消息，以便导航功能包集能获得速度信息。 message so that the navigation stack can get velocity information from it. We'll set the header of the message to the current_time and the "odom" coordinate frame.)
    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = begin;
    odom.header.frame_id = "odom";

    //使用里程计数据填充nav_msgs/Odometry消息并发送出去。 我们将该消息子坐标系为"base_link"，因为我们发布的速度信息要给到该坐标系。                
    //set the position
    odom.pose.pose.position.x = x;
    odom.pose.pose.position.y = y;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = odom_quat;
            
    //set the velocity
    odom.child_frame_id = "base_link";
    odom.twist.twist.linear.x = vx;
    odom.twist.twist.linear.y = vy;
    odom.twist.twist.angular.z = vth;

    //填充机器人的位置、速度，然后发布消息
    //publish the message
    odom_pub.publish(odom);
}

ros::Subscriber sub1;
ros::Subscriber sub;
ros::Subscriber sub2;
void setOdomSubscribe(ros::NodeHandle n,odomCallBack odomCallBackFunc) //
{
    	// 订阅激光里程话题
	//sub1 = n.subscribe("/OdomCorrecting", 1000, odomCallBackFunc);
}

void setMotorSubscribe(ros::NodeHandle n,motorCallBack chatterCallback)
{
    sub = n.subscribe("/cmd_vel", 1000, chatterCallback);							
}

void setDevSubscribe(ros::NodeHandle n, devCallBack devCallback)
{
    sub2 = n.subscribe("/dev_ctl", 1000, devCallback);					
}

/*
void ImuDataSubscribe(ros::NodeHandle n,imucallback imucallback)
{
	sub3 = n.subscribe("/Dev_imu", 1000, imucallback);
}

void DecodeSubscribe(ros::NodeHandle n, decodecallback decodecallback)
{
	sub4 = n.subscribe("/Dev_decode", 1000, decodecallback);
}

*/












