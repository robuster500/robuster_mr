#define _PID_C

#include "pid.h"
#include <math.h>

#define MAXOUT (180)				//输出最大值
#define MINOUT (-180)				//输出最大值

PID sPID;
pPID sptr;
void IncPIDInit(void)
{
	sptr			= &sPID;
	sptr->SetPoint	= 0;		//设定值
	sptr->BitMove	= 0;		//返回结果比例

	sptr->LastError = 0;		//前2次误差值
	sptr->PrevError = 0;		//前1次误差值

	sptr->Proportion = 0.002;        //比例
	sptr->Integral	 = 0;	        //积分
	sptr->Derivative = 0.01;		//微分

	sptr->iError = 0;			//当前误差
	sptr->iIncpid=0;			//增量误差

	sptr->Uk = 0;				//输出返回值
}

void IncPidSetPoint(float setPoint)
{
	sptr->SetPoint = setPoint;
}

float IncPIDCalc(float NextPoint)
{
	//当前误差
	sptr->iError = sptr->SetPoint - NextPoint;
	//增量误差
	sptr->iIncpid= sptr->Proportion * sptr->iError
				- sptr->Integral * sptr->LastError
				+ sptr->Derivative * sptr->PrevError;
	//存储误差，用于下次计算
	sptr->PrevError = sptr->LastError;
	sptr->LastError = sptr->iError;

	sptr->Uk += sptr->iIncpid;

    //输出值限幅
    if ((sptr->Uk) >= MAXOUT)
    {
        sptr->Uk = MAXOUT;
    }
    else if((sptr->Uk) <= MINOUT)
    {
        sptr->Uk = MINOUT;
    }

	return(sptr->Uk);
}






