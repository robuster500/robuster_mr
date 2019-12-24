#ifndef _PID_H

typedef struct PID
{
	float SetPoint;
	
	unsigned char BitMove;
	
	float Proportion;
	float Integral;
	float Derivative;
	
	float iError;
	float iIncpid;
	
	float LastError;
	float PrevError;
	
	float Uk;
}PID,*pPID;


extern void     IncPidSetPoint(float setPoint);
extern void     IncPIDInit(void);
extern float    IncPIDCalc(float NextPoint);

#endif
