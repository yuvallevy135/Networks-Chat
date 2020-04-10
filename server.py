##
# Created by Yuval Levy and Eithan Ker 22/11/2019.
#

from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
source_ip = '127.0.0.1'
source_port = 7946
s.bind((source_ip, source_port))
newData = ""
names_list = []
dic_message = {}  # port : list
dic_names = {}  # port : name

while True:
    data, sender_info = s.recvfrom(2048)
    newData = data.decode()
    # checking validation of the string.
    if len(newData) != 1:
        if newData[1] != ' ' and newData[1] != '\0':
            is_valid = 0
        else:
            is_valid = 1
    else:
        if newData != "1" and newData != "2" and newData != "3" and newData != "4" and newData != "5":
            is_valid = 0
        else:
            is_valid = 1
    if is_valid == 1:
        messNum = newData[0]
        restMes = newData[2:]
        names_list = []
        # checking if the client is already joined the group.
        if sender_info[1] in dic_names:
            sender_inside = 1
        else:
            sender_inside = 0
        # 1 = joining option
        if messNum == "1":
            if sender_inside == 0:
                joinedMes = restMes + " has joined"
                # adding mes to every client to pending list
                for message in dic_message:
                    dic_message[message].append(joinedMes)
                # making list of names
                for name in dic_names:
                    names_list.append(dic_names[name])
                newData = ", ".join(names_list)
                # creating new pending list to the pending list dic, and adding the new client name.
                dic_message[sender_info[1]] = []
                dic_names[sender_info[1]] = restMes
                sender_inside = 1
            else:
                newData = "Illegal request"
        if sender_inside == 1:
            # sending a message to the group.
            if messNum == "2":
                sender_name = dic_names[sender_info[1]]
                joinedMes = sender_name + ": " + restMes
                # adding mes to every client to pending list
                for message in dic_message:
                    if message != sender_info[1]:
                        dic_message[message].append(joinedMes)
            # changing name.
            if messNum == "3":
                sender_name = dic_names[sender_info[1]]
                joinedMes = sender_name + " changed his name to " + restMes
                # adding mes to every client to pending list
                for message in dic_message:
                    if message != sender_info[1]:
                        dic_message[message].append(joinedMes)
                dic_names[sender_info[1]] = restMes
            # leaving the group.
            if messNum == "4":
                sender_name = dic_names[sender_info[1]]
                joinedMes = sender_name + " has left the group"
                # adding mes to every client to pending list
                for message in dic_message:
                    if message != sender_info[1]:
                        dic_message[message].append(joinedMes)
                dic_message.pop(sender_info[1])
                dic_names.pop(sender_info[1])
                newData = ""
            # sending all the pending messages for the client.
            if messNum == "5" or messNum == "2" or messNum == "3":
                newData = "\n".join(dic_message[sender_info[1]])
                dic_message[sender_info[1]].clear()
        else:
            newData = "Illegal request"
    # the request i'snt legal, because the string i'snt legal.
    else:
        newData = "Illegal request"
    s.sendto(newData.encode(), sender_info)  # ack
