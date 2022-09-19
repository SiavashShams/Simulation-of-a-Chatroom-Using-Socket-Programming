import socket
import re
first=1
task=0
sflag=0
wrong=0
regex = re.compile('[^a-zA-Z]')
client_socket = socket.socket()
port = 9000
client_port=int(input("Enter your port number : "))
client_socket.bind(('127.0.0.1', client_port))
client_socket.connect(('127.0.0.1', port))
# recieve connection message from server
recv_msg: bytes = client_socket.recv(1024)
print(recv_msg)
# send user details to server
send_msg = input("Enter your user name(prefix with #):").encode()
client_name = regex.sub('', send_msg.decode())
client_socket.send(send_msg)
# receive and send message from/to different user/s
while True:
    try:

        if(task!='3' and wrong!=1):
            recv_msg = client_socket.recv(1024)
            print(recv_msg.decode())
        task = input("What do you want to do? 1:list 2:send 3:receive 4:exit ")
        wrong=0
        if (task == '1'):
            client_socket.send("List".encode())
            client_socket.send(client_name.encode())


        elif (task == '2'):
            send_msg = input("Send your message in format [@user:message] ")
            if send_msg.startswith("@"):
                client_socket.send(send_msg.encode())
                client_socket.send(client_name.encode())
            else:
                print("Wrong format")
                wrong=1

        elif task=='3':
            recv_msg = client_socket.recv(1024)
            print(recv_msg.decode())
        elif task == '4':
            client_socket.send("Exit".encode())
            client_socket.send(client_name.encode())
            break;
        else:
            print("Command unknown")
            wrong=1
    except:
        continue

client_socket.close()
