/*
 * send_goals.cpp
 *
 *  Created on: Aug 7, 2019
 *      Author: linzhibin
 */

#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_datatypes.h>
#include "geometry_msgs/Point.h"
#include "geometry_msgs/PoseStamped.h"
#include "std_msgs/Header.h"
#include <vector>
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;//<>里面是消息类型

using namespace std;

int main(int argc, char** argv) {

	

	//char *robot_id = argv[1];

	ros::init(argc, argv, "send_goals");
	ros::NodeHandle nh;

	ros::Publisher pub_goal=nh.advertise<geometry_msgs::PoseStamped>("move_base_simple/goal_num",1);
	ros::Rate loop_rate(2);
	int goal_length;
	nh.param("goal_length", goal_length, 1);

	string move_base_str = "/move_base";
	double goal_x=1.0;
	double goal_y=1.0;
	double goal_theta=0;
	// create the action client
	MoveBaseClient ac(move_base_str, true);

	// Wait for the action server to become available
	ROS_INFO("Waiting for the move_base action server");
	ac.waitForServer(ros::Duration(5));

	ROS_INFO("Connected to move base server");

	
	move_base_msgs::MoveBaseGoal goal;
	goal.target_pose.header.frame_id = "map";
	goal.target_pose.header.stamp = ros::Time::now();

	goal.target_pose.pose.position.x = goal_x;
	goal.target_pose.pose.position.y = goal_y;

	// Convert the Euler angle to quaterniond
	double radians = goal_theta * (M_PI/180);
	tf::Quaternion quaternion;
	quaternion = tf::createQuaternionFromYaw(radians);

	geometry_msgs::Quaternion qMsg;
	tf::quaternionTFToMsg(quaternion, qMsg);
	goal.target_pose.pose.orientation = qMsg;

	ROS_INFO("Sending goal to robot : x = %f, y = %f, theta = %f", goal_x, goal_y, goal_theta);
	//ac.sendGoal(goal);

       

	geometry_msgs::PoseStamped pt;
	std::vector<geometry_msgs::PoseStamped> temp;
	ros::Time currentTime = ros::Time::now();

	pt.header.stamp=currentTime;
	pt.header.frame_id = "map";
	/*
	double goal_x0, goal_y0,goal_theta0;
	if (!nh.getParam("goal_x0", goal_x0))
	    goal_x0 = 4.67;
	if (!nh.getParam("goal_y0", goal_y0))
	    goal_y0 = -1.58;
	pt.pose.position.x=goal_x0;
	pt.pose.position.y=goal_y0;
	temp.push_back(pt);
    */
	//Publish a series of target points for path planning
	double goal_x1, goal_y1;
	if (!nh.getParam("goal_x1", goal_x1))
	    goal_x1 = 4.67;
	if (!nh.getParam("goal_y1", goal_y1))
	    goal_y1 = -1.58;
	pt.pose.position.x=goal_x1;
	pt.pose.position.y=goal_y1;
	temp.push_back(pt);
	// if (!nh.getParam("goal_theta", goal_theta))
	//     goal_theta = 0;
/*    double goal_x2, goal_y2;
	if (!nh.getParam("goal_x2", goal_x2))
	    goal_x2 = 0;
	if (!nh.getParam("goal_y2", goal_y2))
	    goal_y2 = -1.58;
	pt.pose.position.x=goal_x2;
	pt.pose.position.y=goal_y2;
	temp.push_back(pt);

	double goal_x3, goal_y3;
	if (!nh.getParam("goal_x3", goal_x3))
	    goal_x3 = 0;
	if (!nh.getParam("goal_y3", goal_y3))
	    goal_y3 = 0.1;
	pt.pose.position.x=goal_x3;
	pt.pose.position.y=goal_y3;
	temp.push_back(pt);*/

/*	double goal_x4, goal_y4;
	if (!nh.getParam("goal_x4", goal_x4))
	    goal_x4 = -4.08;
	if (!nh.getParam("goal_y4", goal_y4))
	    goal_y4 = 0.1;
	pt.pose.position.x=goal_x4;
	pt.pose.position.y=goal_y4;
	temp.push_back(pt);

	double goal_x5, goal_y5;
	if (!nh.getParam("goal_x5", goal_x5))
	    goal_x5 = -4.08;
	if (!nh.getParam("goal_y5", goal_y5))
	    goal_y5 = 2.6;
	pt.pose.position.x=goal_x5;
	pt.pose.position.y=goal_y5;
	temp.push_back(pt);

	double goal_x6, goal_y6;
	if (!nh.getParam("goal_x6", goal_x6))
	    goal_x6 = 0;
	if (!nh.getParam("goal_y6", goal_y6))
	    goal_y6 = 2.6;
	pt.pose.position.x=goal_x6;
	pt.pose.position.y=goal_y6;
	temp.push_back(pt);		

	double goal_x7, goal_y7;
	if (!nh.getParam("goal_x7", goal_x7))
	    goal_x7 = 4.67;
	if (!nh.getParam("goal_y7", goal_y7))
	    goal_y7 = 2.6;
	pt.pose.position.x=goal_x7;
	pt.pose.position.y=goal_y7;
	temp.push_back(pt);
	//p=temp.at(0);
	
	double goal_x8, goal_y8;
	if (!nh.getParam("goal_x8", goal_x8))
	    goal_x8 = 4.67;
	if (!nh.getParam("goal_y8", goal_y8))
	    goal_y8 = 2.6;
	pt.pose.position.x=goal_x8;
	pt.pose.position.y=goal_y8;
	temp.push_back(pt);
	//p=temp.at(0);

	double goal_x9, goal_y9;
	if (!nh.getParam("goal_x9", goal_x9))
	    goal_x9 = 4.67;
	if (!nh.getParam("goal_y9", goal_y9))
	    goal_y9 = 2.6;
	pt.pose.position.x=goal_x9;
	pt.pose.position.y=goal_y9;
	temp.push_back(pt);
	//p=temp.at(0);

	double goal_x10, goal_y10;
	if (!nh.getParam("goal_x10", goal_x10))
	    goal_x10 = 4.67;
	if (!nh.getParam("goal_y10", goal_y10))
	    goal_y10 = 2.6;
	pt.pose.position.x=goal_x10;
	pt.pose.position.y=goal_y10;
	temp.push_back(pt);
	//p=temp.at(0);

	/*double goal_x11, goal_y11;
	if (!nh.getParam("goal_x11", goal_x11))
	    goal_x11 = 4.67;
	if (!nh.getParam("goal_y11", goal_y11))
	    goal_y11 = 2.6;
	pt.pose.position.x=goal_x11;
	pt.pose.position.y=goal_y11;
	temp.push_back(pt);
	//p=temp.at(0);*/

/*	double goal_x12, goal_y12;
	if (!nh.getParam("goal_x12", goal_x12))
	    goal_x12 = 4.67;
	if (!nh.getParam("goal_y12", goal_y12))
	    goal_y12 = 2.6;
	pt.pose.position.x=goal_x12;
	pt.pose.position.y=goal_y12;
	temp.push_back(pt);*/
	//p=temp.at(0);

	
	for (int i = 0; i < temp.size(); i++)
	{
		/* code for loop body */
		//ROS_INFO("temp.size()=%d",temp.size());
		//ROS_INFO("temp.at(i)=%f",temp.at(i).pose.position.x);
		pt=temp.at(i);
		ROS_INFO("pt.x=%f,pt.y=%f",pt.pose.position.x,pt.pose.position.y);
		pub_goal.publish(pt);
		
		loop_rate.sleep();
	}
    // Send a goal to move_base
	ac.sendGoal(goal);
	ros::spin();
	return 0;
}



