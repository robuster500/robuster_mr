#ifndef ROBUSTER_DEV_NODE_H
#define ROBUSTER_DEV_NODE_H

typedef void (*imuFuncCallabck)(float angle,float rate);
typedef void (*decodeFuncCallabck)(short speed_l,short speed_r,int mile_l,int mile_r);




extern int          initRobusterDev(int brund);
extern void         setDecodeCallBack(decodeFuncCallabck decodeCallback);
extern void         setImuCallBack(imuFuncCallabck imuCallback);
extern void         loopRobusterDev(void);
extern void         setDevRunSpeed(short speed_l,short speed_r);

#endif
