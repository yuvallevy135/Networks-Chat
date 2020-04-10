##
# Created by Yuval Levy and Eithan Ker 22/11/2019.
#
from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
dest_ip = '127.0.0.1'
dest_port = 7946
msg = 0
while not msg == '4':
    msg = input("Message to send:")
    s.sendto(msg.encode(), (dest_ip, dest_port))
    data, sender_info = s.recvfrom(2048)
    print(data.decode())
s.close()