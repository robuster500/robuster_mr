#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int32MultiArray.h"
#include "std_msgs/UInt32MultiArray.h"
//#include "std_msgs/Float32MultiArray.h"
#include <geometry_msgs/Twist.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include "tf/transform_datatypes.h"
#include <boost/thread.hpp>
#include "robuster_node_ros.h"
#include "math.h"
#define LINEAR_X_MAX	3.0

#define ANGULAR_Z_MAX	2.8 

#define TURN_PARAM	0.10

#define REDUCTION_RATIO	20     //MR1000--31.345


#define WHEEL_DIAMETER	0.203     //MR1000--0.29

#define PI	3.14159


double g_sigma = 1.04;

//定义导航的激光里程校准（只底层调用可以忽略）
float laser_x, laser_y;
float laser_z;
geometry_msgs::Quaternion laser_odom_quat;
tf::Quaternion quat;
ros::Publisher WheelSpeed_pub;
//默认机器人的起始位置是odom参考系下的0点	
double x = 0.0;
double y = 0.0;
double z = 0.0;
double yaw = 0.0;
double pitch = 0.0;
double roll = 0.0;


float sg_aimAngle=0.0;
float sg_angle1=0.0;
static float sg_angle;

//机器人在base_link参考系下的前进旋转速度
double vx = 0;
double vy = 0;
double vth = 0; 

double sg_delta_x = 0;
double sg_delta_y = 0;

double sg_delta_x_speed = 0;
double sg_delta_y_speed = 0;
double pose_th = 0;
double pose_theta = 0;
float linear_max_x,angular_max_z;
double yaw_start,yaw_now, yaw_use,pre_yaw;
double mile_l_start, mile_r_start, mile_l_use, mile_r_use;

void setspeedback(float linear_x_speed, float angular_z_speed);
void setInitAnglePid(float aimAngle,float curAngel);

void odomCallbackFunc(const nav_msgs::Odometry& msg)
{
	laser_x = msg.pose.pose.position.x;
	laser_y = msg.pose.pose.position.y;
	laser_z = msg.pose.pose.position.z;
	laser_odom_quat = msg.pose.pose.orientation;
    tf::quaternionMsgToTF(msg.pose.pose.orientation,quat);
}


//电机控制回调函数 
void chatterCallback(const geometry_msgs::Twist& msg)
{

	linear_max_x = msg.linear.x;
	angular_max_z = msg.angular.z;
	//printf("linear_max_x = %f angular_max_z = %f\r\n",linear_max_x,angular_max_z);
	setspeedback(linear_max_x,angular_max_z);
}
//设备控制回调函数
void devCtlCallback(const nav_msgs::Odometry& msg)
{
   sg_aimAngle=msg.pose.pose.position.x;
   sg_angle1=msg.pose.pose.position.y;
   sg_aimAngle=(sg_aimAngle/PI)*180;
   sg_angle1=(sg_angle1/PI)*180;
   //printf("sg_aimAngle= %f sg_angle1 = %f\r\n",sg_aimAngle,sg_angle1);
   //setInitAnglePid(sg_aimAngle,sg_angle);
   
}
//平台绕Z轴转速转换为左右轮差速
float yawrate_to_speed(float yawrate)
{
	float theta_to_speed, speed_ret;
	theta_to_speed = TURN_PARAM;
	//yawrate: rad/s  ,*0.1 表示100ms内转动的弧度 ，/theta_to_speed 是把要转的弧度转换为左右轮子速度差
	speed_ret = (yawrate * 0.1) / theta_to_speed;
	return speed_ret;
}

void setspeedback(float linear_x_speed, float angular_z_speed)
{
	float linear_x, angular_z;
	 std_msgs::UInt32MultiArray msg1;
	
	if(linear_x_speed > LINEAR_X_MAX )
	{
		linear_x = LINEAR_X_MAX;	
	}
	else if(linear_x_speed <  -LINEAR_X_MAX)
	{
		linear_x = -LINEAR_X_MAX;		
	}
	else
	{
		linear_x = linear_x_speed;
	}

	if(angular_z_speed > ANGULAR_Z_MAX )
	{
		angular_z = ANGULAR_Z_MAX;	
	}
	else if(angular_z_speed < -ANGULAR_Z_MAX)
	{
		angular_z =- ANGULAR_Z_MAX;		
	}
	else
	{
		angular_z = angular_z_speed ;
	}

	float yawspeed;
	float Lwheelspeed, Rwheelspeed;
	float cent_speed = linear_x;

	//将转速转为电机差速
	yawspeed = yawrate_to_speed(angular_z);

	//算出左右电机轮速，单位m/s
	Lwheelspeed = cent_speed - yawspeed/2;
	Rwheelspeed = cent_speed + yawspeed/2;

	//算出左右电机转速，单位:tik/ms(1r=10000tk)
	static float para = (REDUCTION_RATIO * 65535) / (WHEEL_DIAMETER * PI * 1000 );
	int speed_l =(int)(Lwheelspeed * para);
	int speed_r =(int)(Rwheelspeed * para);

	//设置电机转速
	printf("lspeed = %d rspeed = %d,parm = %f\r\n",speed_l,speed_r,para);
	//发布速度
        
        msg1.data.push_back(speed_l);
	
	msg1.data.push_back(speed_r);
	WheelSpeed_pub.publish(msg1);
	
	//setDevRunSpeed(speed_l, speed_r);
}

static float sg_rate;
static int sg_imuflg = 0;

static int sg_l_mile;
static int sg_r_mile;
static short sg_l_speek;
static short sg_r_speek;
static int sg_decodeflg = 0;
static int sg_int_angle;
static int sg_int_rate;

void decodecallback(const std_msgs::UInt32MultiArray& pubdecode)
{
	sg_l_speek = (short)(((short)pubdecode.data[0]) / 65535);
	sg_r_speek = (short)(((short)pubdecode.data[1]) / 65535);
	sg_l_mile = pubdecode.data[2];
	sg_r_mile = pubdecode.data[3];

	sg_decodeflg = 1;
	//printf("mile_l = %d, mile_r = %d\r\n",pubdecode.data[0], pubdecode.data[1]);
}

double g_rateSpeed = 0;

void imucallback(const std_msgs::UInt32MultiArray& pubimu)
{
	sg_int_angle = (int)pubimu.data[0];
	sg_int_rate = (int)pubimu.data[1];
	sg_angle = ((float)sg_int_angle) / 10000 ;
	sg_rate = ((float)sg_int_rate) / 10000 ;
	sg_imuflg = 1;
	//printf("imu = %f, rate= %f\r\n",sg_angle, sg_rate);
}


double sg_delta_theta ;
void orientationcalculate(float angle)
{
	
	double yaw_now = (double)angle;
	//get current jiaodu 
	pose_th = pose_theta;
	
	yaw_use = yaw_now - pre_yaw;

	pre_yaw = yaw_now;
	//get diff delta
	sg_delta_theta = -yaw_use * PI / 180;
	g_rateSpeed = -sg_rate * PI / 180;
	//clac current theta
	pose_theta += sg_delta_theta;

}

void positioncalculate(int mile_l,int mile_r, double delta_theta, double pose_th)
{
	double mile_l_now = (double)mile_l;
	double mile_r_now = (double)mile_r;


	mile_l_use = mile_l_now - mile_l_start;
	mile_r_use = mile_r_now - mile_r_start;
	//printf("mile_l_use=%f,mile_r_use=%f\n",mile_l_use,mile_r_use); 

	mile_l_start = mile_l_now;
	mile_r_start = mile_r_now;

	// r/s 
	double l_go_distance_speed = ((double)(sg_l_speek)*(PI * WHEEL_DIAMETER) / REDUCTION_RATIO) ;
	double r_go_distance_speed = ((double)(sg_r_speek)*(PI * WHEEL_DIAMETER) / REDUCTION_RATIO) ;

	double l_go_distance = mile_l_use * PI * WHEEL_DIAMETER * g_sigma/(65535 * REDUCTION_RATIO );
	double r_go_distance = mile_r_use * PI * WHEEL_DIAMETER * g_sigma/(65535 * REDUCTION_RATIO );
	double rotate_radius;
	double rotate_radius_speed;
	double change_x, change_y;
	double change_x_speed, change_y_speed;
	if(delta_theta != 0)
	{
		rotate_radius = (l_go_distance + r_go_distance) / (2.0 * delta_theta);
		change_x = rotate_radius * sin(delta_theta);
		change_y = rotate_radius * (1 - cos(delta_theta));

		rotate_radius_speed = (l_go_distance_speed + r_go_distance_speed) / (2.0 * delta_theta);
		change_x_speed = rotate_radius_speed * sin(delta_theta);
		change_y_speed = rotate_radius_speed * (1 - cos(delta_theta));
	}
	else
	{
			change_x = (l_go_distance + r_go_distance) / 2.0;
			change_y = 0;

			change_x_speed = (l_go_distance_speed + r_go_distance_speed) / 2.0;
			change_y_speed = 0;			
	}
	sg_delta_x_speed = change_x_speed * cos(-pose_th) + change_y_speed * sin(-pose_th);
	sg_delta_y_speed = change_y_speed * cos(-pose_th) - change_x_speed * sin(-pose_th);

	if(sg_l_speek + sg_r_speek > 0)
		sg_delta_x_speed = fabs(sg_delta_x_speed);
	else if(sg_l_speek + sg_r_speek < 0)
	{
		sg_delta_x_speed = fabs(sg_delta_x_speed) * -1;
	}
	printf("xspeed = %lf\r\n",sg_delta_x_speed);	

	if(fabs(sg_l_speek) > fabs(sg_r_speek))
		sg_delta_y_speed = fabs(sg_delta_y_speed);
	else if(fabs(sg_l_speek) < fabs(sg_r_speek))
	{
		sg_delta_y_speed = fabs(sg_delta_y_speed) * -1;
	}
	
	sg_delta_x = change_x * cos(-pose_th) + change_y * sin(-pose_th);
	sg_delta_y = change_y * cos(-pose_th) - change_x * sin(-pose_th);

	x += sg_delta_x;
	y += sg_delta_y;

	
}


void velocitycalculate(double delta_x, double delta_y, double delta_theta,double dt)
{
	vx = delta_x;
	vy = delta_y;
	vth = g_rateSpeed;
}





/****************************************************/

/****************************************************/
static int sg_initDecode = 0;
int main(int argc, char **argv)
{	
	ros::init(argc, argv, "robuster_node_mile");
	ros::NodeHandle n;

	ros::Rate loop_rate(100);//100HZ的发布频率
	ros::Publisher odom_pub ;
	
        WheelSpeed_pub= n.advertise<std_msgs::UInt32MultiArray>("WheelSpeed", 1000);

	initNodeRos(odom_pub,n);
    //定义一个tf广播，来发布tf变化信息
    tf::TransformBroadcaster odom_broadcaster;  
	//设置数据回调函数
	setMotorSubscribe(n,chatterCallback);
	setOdomSubscribe(n,odomCallbackFunc);
	setDevSubscribe(n,devCtlCallback);
	//ImuDataSubscribe(n,imucallback);
	//DecodeSubscribe(n, decodecallback);
	ros::Subscriber sub3 = n.subscribe("/Dev_imu", 1000, imucallback);
	ros::Subscriber sub4 = n.subscribe("/Dev_decode", 1000, decodecallback);
	
	//获取当前时间用于计算瞬时速度和角度
	ros::Time current_time, last_time;
	current_time =ros::Time::now();
	last_time = ros::Time::now();

	short l_speed,r_speed;

	while(1)
	{	
		if(loopNodeRos() == 0)
		{
			break;
		}
	    loop_rate.sleep();
		//loopRobusterDev();
		if(sg_imuflg !=0 && sg_decodeflg != 0)
		{
			///*
			//*/
			if( sg_initDecode == 0)
			{
				sg_initDecode = 1;
				yaw_start = sg_angle;
				pre_yaw = yaw_start;
				mile_l_start = (double)sg_l_mile;
				mile_r_start =  (double)sg_r_mile;
     			//printf("sg_aimAngle=%f,sg_angle1=%f\n",sg_aimAngle,sg_angle1);	
				//setInitAnglePid(sg_aimAngle,sg_angle1);
				//setInitAnglePid(sg_aimAngle,sg_angle);
			}
			sg_imuflg = 0;
			sg_decodeflg = 0;

			orientationcalculate(sg_angle);
			positioncalculate(sg_l_mile,sg_r_mile,sg_delta_theta,pose_th);
	

			current_time = ros::Time::now();
			double dt = (current_time - last_time).toSec();
			velocitycalculate(sg_delta_x_speed, sg_delta_y_speed, sg_delta_theta,dt);
			pushMailData(odom_pub,odom_broadcaster,pose_theta, x, y, vx, vy, vth);
			last_time = current_time;
		}
		
	}
	return 0;
}














