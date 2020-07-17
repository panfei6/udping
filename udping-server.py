# # -*- coding: utf-8 -*-
# import socket
# ADDRESS="127.0.0.1"
# PORT=1234
#
# while True:
#     print("waitting for package...")
#     s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     s.bind((ADDRESS,PORT))
#     data=s.recv(1024)
#     print("received package"+data.decode()+"form")
#     addr = s.recvfrom(1024)
#     content = "hello world"
#     s.sendto(content.encode('utf-8'), addr)

import socket
import select
def udpserver():
    # 1创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(0.1)
    # 2.绑定一个本地信息
    localaddr = ("127.0.0.1",1234) # 必须绑定自己电脑IP和port
    udp_socket.bind(localaddr)
    # 3.接收数据
    while True:
        try:
            udp_socket.settimeout(0.1)
            recv_data = udp_socket.recvfrom(1024)
            # recv_data存储元组（接收到的数据，（发送方的ip,port））
            recv_msg = recv_data[0] # 信息内容
            send_addr = recv_data[1] # 信息地址
            # 4.打印接收到的数据
            # print("from %s messages :%s" %(str(send_addr),recv_msg.decode("utf-8")))
            logfile = open("/var/log/udplisten.log", "a")
            logfile.write("from %s messages :%s\n" % (str(send_addr), recv_msg.decode("utf-8")))
            logfile.close()
            udp_socket.sendto("ok".strip().encode("utf-8"), send_addr)
        except Exception as e:
            pass

if __name__ == "__main__":
    udpserver()
