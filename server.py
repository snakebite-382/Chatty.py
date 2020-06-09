import socket
import select

HEADER_LENGTH = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

print("server started")

def recieve_message(client_socket):
	message_header = client_socket.recv(HEADER_LENGTH)

	if not len(message_header):
		return False

	message_length = int(float(message_header.decode('utf-8').strip()))
	return {'header': message_header, 'data': client_socket.recv(message_length)}

while True:
	read_sockets, _x_, exception_sockets = select.select(sockets_list, [], sockets_list) 
	
	for notified_socket in read_sockets:
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()
			print("accepted")

			user = recieve_message(client_socket)
			
			print(user)
			print("Recieved")
			
			if(not user):
				continue

			sockets_list.append(client_socket)
			print("added to list")

			clients[client_socket] = user
			print("created user")

			print(f"Accepted connection from {client_address[0]}{client_address[1]} username: {user['data'].decode('utf-8')}")

		else:
			message = recieve_message(notified_socket)

			if(message is False):
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			else:
			 	user = clients[notified_socket]

			 	type_, data = message['data'].decode("utf-8").split("$")


			 	if(type_ == "message"):
				 	print(f"Recieved Message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')} of type {type_}")
				 	for client_socket in clients:

				 		if client_socket != notified_socket:
				 			client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]	
		print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}") 			
