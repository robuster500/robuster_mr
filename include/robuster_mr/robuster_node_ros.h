#ifndef ROBUSTER_NODE_ROS_H
#define ROBUSTER_NODE_ROS_H

#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>
#include "tf/transform_datatypes.h"
#include "robuster_node_mile.h"

typedef  void (*odomCallBack)(const nav_msgs::Odometry& msg);
typedef  void (*motorCallBack)(const geometry_msgs::Twist& msg);
typedef  void (*devCallBack)(const nav_msgs::Odometry& msg);

extern void setOdomSubscribe(ros::NodeHandle n,odomCallBack odomCallBackFunc);
extern void setMotorSubscribe(ros::NodeHandle n,motorCallBack chatterCallback);
extern void setDevSubscribe(ros::NodeHandle n,devCallBack devCallback);

extern void initNodeRos(ros::Publisher &odom_pub,ros::NodeHandle n);
extern int loopNodeRos();

extern void pushMailData(ros::Publisher odom_pub,tf::TransformBroadcaster odom_broadcaster,double pose_theta,double x, double y, double vx, double vy, double vth);



#endif
