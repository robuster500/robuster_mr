#ifndef MR1000LIB_H
#define MR1000LIB_H
#include <iostream>
using namespace std;


#define uint8_t unsigned char
#define uint16_t unsigned short
//�������ݰ���Ϣ

#define SZZQ_ROBOT_HEART_CONN         0x00
#define SZZQ_ROBOT_HEART_DISCON       0x01

//����ָ����Ϣ

#define SZZQ_ROBOT_CTL_EN             0x01
#define SZZQ_ROBOT_CTL_DISEN          0x00

//����ָ����Ϣ

#define SZZQ_ROBOT_WARNING_TEM        0x80
#define SZZQ_ROBOT_WARNING_HUM        0x40
#define SZZQ_ROBOT_WARNING_CAR        0x20
#define SZZQ_ROBOT_WARNING_MOTOR      0x10

//�������ָ����Ϣ

#define SZZQ_ROBOT_MOTOR_FOR          0x00
#define SZZQ_ROBOT_MOTOR_BAK          0x01
#define SZZQ_ROBOT_MOTOR_LEFT         0x00
#define SZZQ_ROBOT_MOTOR_RIGHT        0x01

//LED����ָ����Ϣ

#define SZZQ_ROBOT_LIGHT_OPEN         0x01
#define SZZQ_ROBOT_LIGHT_CLOSE        0x00

//פ��ָ����Ϣ

#define SZZQ_ROBOT_MOTOR_PARK_EN      0x00
#define SZZQ_ROBOT_MOTOR_PARK_DIS     0x01

//�ϱ��ظ�����

#define SZZQ_ROBOT_MOTOR_SUCCESS       0x00
#define SZZQ_ROBOT_MOTOR_FALSE         0x01
#define SZZQ_ROBOT_MOTOR_REV_SUCCESS   0x02
#define SZZQ_ROBOT_MOTOR_PARM_ERROR    0x03


//�豸�����ϱ�����

enum SZZQ_ROBOT_CMD
{
     SZZQ_ROBOT_HEART_FUNCODE     = (0x0101),
     SZZQ_ROBOT_CTL_FUNCODE       = (0x0102),
     SZZQ_ROBOT_WARNING_FUNCODE   = (0x0103),
     SZZQ_ROBOT_NOPID_FUNCODE     = (0x0201),
     SZZQ_ROBOT_PID_FUNCODE       = (0x0202),
     SZZQ_ROBOT_LIGHT_FUNCODE     = (0x0203),
     SZZQ_ROBOT_PARK_FUNCODE      = (0x0204),
     SZZQ_ROBOT_REPLY_FUNCODE     = (0x0205),
     SZZQ_ROBOT_DEVINFO_FUNCODE   = (0x0206),     
};
enum SZZQ_DEV_CMD
{
     SZZQ_DEV_WARNING_CMD        =    (0xA001),
     SZZQ_DEV_CTL_CMD            =    (0xA002),
     SZZQ_DEV_GET_CMD            =    (0xA003),
     SZZQ_DEV_HEART_CMD          =    (0xA004),
     SZZQ_DEV_REPLY_CMD          =    (0xA005),
     SZZQ_DEV_DEVINFO_CMD        =    (0xA006),     

     SZZQ_DEV_IMU_CMD            =    (0xA101),
     SZZQ_DEV_DECODE_CMD         =    (0xA102),
     SZZQ_DEV_CSB_CMD            =    (0xA103),
     SZZQ_DEV_INFO_CMD           =    (0xA104),
};

enum rpyStatus
{
    SUCCESS,
    ERROR,
};

//�ͻ�ʵ��
extern void setHeartStatus(uint8_t status);
extern void setWarningStatus(uint8_t status);
extern void setIMUData(uint8_t* buff);
extern void setDecodeData(uint8_t *buff);
extern void setReply(uint16_t cmd,uint8_t status);
extern void setDevStatus(uint8_t *buff);
extern void setDevInfo(uint8_t *buff);
extern void setDevInfoStatus(uint8_t *buff);


rpyStatus   closeSerial(void);
rpyStatus   initMR1000Lib(char *portName,int baud);
void        getSaveDataToClient(void);
rpyStatus   ansyDataForDev(char data);
rpyStatus   readData(char *buff,int &len,int RevBuffLen);

void        sendDevReply(char status);
void        sendDevPark(char status);
void        sendDevLight(char forLight,char forLim,char bakLight,char bakLim);
void        setSpeedForPid(char ForB,char LorR,char rumMode,short Speed,short Direct);
void        setSpeedForNoPid(char lDir,char rDir,char rumMode,short lSpeed,short rSpeed);
void        sendWarning(char warning);
void        sendDevCtl(char ctlMode);
void        sendDevHeart(char status);
void        sendDevInfo(void);
uint16_t    TimeCheck(void);

#endif




