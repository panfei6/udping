# -*- coding: utf-8 -*-
import socket
import sys
import re
import time

ADDRESS = "127.0.0.1"
PORT = 1234
Count = 4

for i in range(0,len(sys.argv)):
    if sys.argv[i] == "-h":
        try:
            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", sys.argv[i+1]):
                ADDRESS = sys.argv[i+1]
            else:
                print("IP address format is incorrect...")
        except IndexError as e:
            print("Missing required parameters...")

    if sys.argv[i] == "-p":
        try:
            PORT = sys.argv[i+1]
        except IndexError as e:
            print("Missing required parameters...")

    if sys.argv[i] == "-c":
        try:
            Count = sys.argv[i+1]
        except IndexError as e:
            print("Missing required parameters...")

def udpclient():
    # ADDRESS = "10.36.3.113"  ## server端IP地址
    # PORT = 1234  ## server端监听端口
    begin = 1  
    FailCount = 0  ## 丢包次数统计
    # Count = 2000  
    arr_ttl = []
    sentdata = "udpsocket sent package to %s" % ADDRESS
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(1)  ## 设置连接超时
    while begin <= int(Count):
        try:
            ttl_begin = time.time()
            udp_socket.sendto(sentdata.encode(), (ADDRESS, PORT))
            udp_socket.setblocking(False)
            udp_socket.settimeout(1)
            msg, address = udp_socket.recvfrom(1024)
            ttl_end = time.time()
            arr_ttl.append(ttl_end-ttl_begin)
            print("64 bytes from %s port=%s: udp_seq=%s msg=%s ttl=%.1fms" % (ADDRESS,PORT,begin,msg.decode('utf-8'),(ttl_end-ttl_begin)*1000))
            begin += 1
            LossRate = float(FailCount) / int(Count) * 100
        except Exception as e:
            FailCount += 1
            print("64 bytes from %s port=%s: udp_seq=%s msg=timeout" % (ADDRESS,PORT,begin))
            begin += 1
            LossRate = float(FailCount) / int(Count) * 100
    print("--- %s statistics ---" % ADDRESS)
    print("%s packets transmitted, %s received, max_ttl=%.1fms, min_ttl=%.1fms, %.2f" % (int(Count),int(Count)-FailCount,min(arr_ttl)*1000,max(arr_ttl)*1000,LossRate) + "% packet loss.")
if __name__ == "__main__":
    udpclient()
