import socket # for creating a server
import select # for managing read and unread sockets
from tkinter import * # for the GUU
import threading # for runnign multiple loops
import time # for telling the time

HEADER_LENGTH = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234

threadList = []

class ServerNoGui():

	def __init__(self):
		# create the socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# start the server
		self.server_socket.bind((IP, PORT))
		self.server_socket.listen()

		# keep track of whos on the server
		self.sockets_list = [self.server_socket]

		self.clients = {}

		# print some starting data about the server
		print("server started")
		serverStartTime = time.ctime()
		window.logData("Starting thread sub-proccesses...")
		self.recieveLoop = threading.Thread(target=self.manageDataSending)
		self.recieveLoop.start()
		window.logData("sub-proccesses started!")

		window.logData(f"Server Started at {serverStartTime} on PORT {PORT} at IP {IP}")
		# update the status
		window.status['text'] = f"[SERVER OPEN AT PORT : {PORT} IP : {IP} NUM_CLIENTS : {len(self.sockets_list)-1}]"

	def statusUpdate():
		window.status['text'] = f"[SERVER OPEN AT PORT : {PORT} IP : {IP} NUM_CLIENTS : {len(self.sockets_list-1)}]"

	def recieve_message(self, client_socket):
		# reveive information about what to receive
		message_header = client_socket.recv(HEADER_LENGTH)

		if not len(message_header):
			return False

		message_length = int(float(message_header.decode('utf-8').strip()))
		# return information about the message
		return {'header': message_header, 'data': client_socket.recv(message_length)}

	def runCommand(self, command):
		# set the username as server
		userData = "server".encode("utf-8")
		userHeader = f"{len(userData):<{HEADER_LENGTH}}".encode("utf-8")

		command = str(command)

		# send the command as the message with the type cmd
		messageData = f"cmd${command}".encode("utf-8")
		messageHeader = f"{len(messageData):< {HEADER_LENGTH}}".encode("utf-8")

		# send
		for client_socket in self.clients:
			client_socket.send(userHeader + userData + messageHeader + messageData)
		window.logData(f"sent server command {command}")
		window.logChat("SERVER",command)



	def acceptUsers(self):
		# accept incoming connections
		# get the sockets to accept
		read_sockets, _x_, exception_sockets = select.select(self.sockets_list, [], self.sockets_list) 
		
		for notified_socket in read_sockets:
			if notified_socket == self.server_socket:
				# accept the connection
				client_socket, client_address = self.server_socket.accept()

				user = self.recieve_message(client_socket)
								
				if(not user):
					continue
				# add them to our collection of clients
				self.sockets_list.append(client_socket)

				self.clients[client_socket] = user

			window.logData(f"Accepted connection from {client_address[0]}{client_address[1]} username: {user['data'].decode('utf-8')}")
	
	def updateStatus(self):
		window.status['text'] = f"[SERVER OPEN AT PORT : {PORT} IP : {IP} NUM_CLIENTS : {len(self.sockets_list)-1}]"

	def manageDataSending(self):
		while True:
			self.updateStatus()
			# check for messages
			read_sockets, _x_, exception_sockets = select.select(self.sockets_list, [], self.sockets_list) 	
			for notified_socket in read_sockets:
				# if the connection is for the server accept a new user
				if notified_socket == self.server_socket:
					self.acceptUsers()
				else:
					# otherwose recieve the message
					message = self.recieve_message(notified_socket)

					if(message is False):
						window.logData(f"Closed connection from {self.clients[notified_socket]['data'].decode('utf-8')}")
						self.sockets_list.remove(notified_socket)
						del self.clients[notified_socket]
						continue

					else:
					 	user = self.clients[notified_socket]

					 	type_, data = message['data'].decode("utf-8").split("$", 1)

					 	# check the type and act properly

					 	if(type_ == "message" and not data.strip() == ""):
						 	window.logData(f"Recieved Message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')} of type {type_}")
						 	window.logChat(user['data'].decode('utf-8'), data)
						 	for client_socket in self.clients:

						 		if client_socket != notified_socket:
						 			window.logData("Sending message")
						 			client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
						 	


class serverGUI():
	def __init__(self):
		# create the window
		self.window = Tk()
		self.window.title(f"Chatt.py HOSTING SERVER (IP : {IP} \\\\ PORT : {PORT})")
		self.window.configure(bg="black")

		self.padSizeX = 5
		self.padSizeY = 60

		# create a list to log server side actions
		self.logText = Listbox(self.window, fg="blue", bg="black", width=50, height=25, selectbackground="blue", highlightcolor="black")
		self.logText.grid(row=1, column=0)

		# create a log of the chat
		self.chatLogText = Listbox(self.window, fg="green", bg="black", width=50, height=25, selectbackground="green", highlightcolor="black")
		self.chatLogText.grid(row=1, column=1)

		# create the command interface
		self.commandInput = Entry(self.window, fg="red", bg="black")
		self.submitButton = Button(self.window, text="Run CMD", command= lambda : serverBackend.runCommand(self.commandInput.get()), fg="red", bg="black", activebackground="black", activeforeground="red")
		self.commandInput.grid(row=2, column=0, columnspan=2)
		self.submitButton.grid(row=3, column=0, columnspan=2)

		# create a status label
		self.status = Label(self.window, text="[NO CONNECTION]", bg="black", fg="white")
		self.status.grid(row=0, column=0, columnspan=2)

	def logData(self, data):
		self.logText.insert(END, data)

	def logChat(self, username, message):
		self.chatLogText.insert(END, f"{username} >> {message}")
# and here's where we call all that stuff creating the app
window = serverGUI()
global serverBackend
serverBackend = ServerNoGui()
window.window.mainloop()
