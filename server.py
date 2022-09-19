import socket,select
port = 9000
socket_list = []
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1',port))
server_socket.listen(5)
socket_list.append(server_socket)
while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            connect.send(("You are connected from:" + str(addr)).encode())
        else:
            try:
                data = sock.recv(2048).decode()
                if data.startswith("#"):
                    users[data[1:].lower()]=connect
                    print ("User " + data[1:] +" added.")
                    print(users)
                    connect.send(("Your user detail saved as : "+str(data[1:])).encode())
                    print("this is connect\n")
                    print(connect)

                elif data.startswith("@"):
                    if data[1:data.index(':')].lower() in users:
                        data2 = sock.recv(2048).decode()
                        users[data[1:data.index(':')].lower()].send((data2+': '+(data[data.index(':')+1:])).encode())
                        users[data2.lower()].send(("Message sent succussfuly! ").encode())

                    else:
                        print("User not found")
                        data2 = sock.recv(2048).decode()
                        users[data2.lower()].send(("User not found ").encode())

                elif data=="List":
                    data = sock.recv(2048).decode()
                    users[data.lower()].send((("List of users : " + str(list(users.keys()))).encode()))

                elif data =="Exit":
                    data = sock.recv(2048).decode()
                    del users[data]
                    print(users)

            except:
                continue
server_socket.close()