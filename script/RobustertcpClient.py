#!/usr/bin/env python3
#-*-coding:utf-8-*-

from socket import *

class RobusterClient:
    tcp_client_socket = ''
    checkCon = 0
    def __init__(self,ip,port):           
        try: 
            self.tcp_client_socket = socket(AF_INET,SOCK_STREAM)
            self.tcp_client_socket.connect((ip,port))  
            self.tcp_client_socket.settimeout(0.01)        
            self.checkCon = 1
        except :
            print("tcp client connect error")

    def writeOpt(self,data):
        try:
            data = bytes(data)
            self.tcp_client_socket.send(data)
            return True
        except :
            print("tcp client send error")
            self.checkCon = 0
            return False
            
    def readOpt(self):       
        try:
            recv_data = self.tcp_client_socket.recv(1024)        
        except:
            return [],0

        if not recv_data:
            self.checkCon = 0
            print("close client")
            return [],0
        else:
            self.checkCon = 1                
            return recv_data,len(recv_data)

    def closeClient(self):
        self.tcp_client_socket.close()
        tcp_client_socket = ""

    def checkClient(self):
        return self.checkCon

# def main():
#     # 1.创建tcp_client_socket 套接字对象
#     tcp_client_socket = socket(AF_INET,SOCK_STREAM)
#     # 作为客户端，主动连接服务器较多，一般不需要绑定端口

#     # 2.连接服务器
#     tcp_client_socket.connect(("192.168.44.88",8080))
#     while True:
#         """无限循环可以实现无限聊天"""
#         # 3.向服务器发送数据
#         meg = input("请输入要发送的消息：")
#         tcp_client_socket.send(meg.encode()) 
#  　　　　　　# 在linux中默认是utf-8编码
#         # 在udp协议中使用的sendto() 因为udp发送的为数据报，包括ip port和数据，
#            # 所以sendto()中需要传入address，而tcp为面向连接，再发送消息之前就已经连接上了目标主机

#         # 4.接收服务器返回的消息
#         recv_data = tcp_client_socket.recv(1024)  # 此处与udp不同，客户端已经知道消息来自哪台服务器，不需要用recvfrom了

#         if recv_data:
#             print("返回的消息为:",recv_data.decode('gbk'))
#         else:
#             print("对方已离线。。")
#             break

#     tcp_client_socket.close()


# if __name__ == '__main__':
#     main()