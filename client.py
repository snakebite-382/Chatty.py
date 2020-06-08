import socket
import select
import errno
import sys
import threading
from tkinter import *


HEADER_LENGTH = 10

IP = socket.gethostbyname("0.0.0.0")
PORT = 1234

class inputNameWin():
	def __init__(self):
		self.window = Tk()
		self.window.title("login")

		self.inputLabel = Label(self.window, text="Type in your username, then click connect")
		self.inputLabel.grid(row=0, column=1)

		self.inputName = Entry(self.window, width="10")
		self.inputName.grid(row=1, column=0, columnspan=2)

		self.connectButton = Button(self.window, text="CONNECT", command= lambda : self.checkName(self.inputName.get()))
		self.connectButton.grid(row=2, column=0, columnspan=2)
		self.window.mainloop()

	def checkName(self, name):
		name = name.strip()
		if len(name) <= 3 :
			self.inputLabel['text'] = f"Username {name} is too short! Try another"
		elif len(name) >= 15:
			self.inputLabel['text'] = f"Username {name} is too long! Try another"
		else:
			self.window.destroy()
			start(name)


class mainWin():
	def __init__(self, username):
		self.username = username
		self.mainWindow = Tk()
		self.mainWindow.title(f"Chatty.py client [NO CONNECTION] NAME = {self.username}")
		self.mainWindow.configure(bg="white")

		self.padSizeX = 5
		self.padSizeY = 60

		self.status = Label(self.mainWindow, text=f"Username : {self.username} [NO CONNECTION]", fg="black", bg="white")
		self.status.grid(row=0, column=0, columnspan=2)

		self.messagEntry = Entry(self.mainWindow, fg="black", bg="white")
		self.messageSend = Button(self.mainWindow, text="Send", command= lambda : connection.sendMessage(self.messagEntry.get()), fg="green", bg="white", activebackground="white", activeforeground="black")
		self.messagEntry.grid(row=2, column=0, columnspan=2)
		self.messageSend.grid(row=3, column=0, columnspan=2)

		self.incoming = Listbox(self.mainWindow, fg="green", bg="white", width=50, height=25, selectbackground="blue", highlightcolor="green2")
		self.incoming.grid(row=1, column=0)

		self.outgoing = Listbox(self.mainWindow, fg="blue", bg="white", width=50, height=25, selectbackground="green", highlightcolor="green2")
		self.outgoing.grid(row=1, column=1)

class connectionHandler():
	def __init__(self, username):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((IP, PORT))
		self.client_socket.setblocking(False)

		self.username = username.encode("utf-8");
		self.username_header = f'{len(username):<{HEADER_LENGTH}}'
		self.username_header = self.username_header.encode('utf-8')

		self.client_socket.send(self.username_header + self.username)

		main = threading.Thread(target=self.main)
		main.start()

	def sendMessage(self,message):
		if(message):
			try:	
				message = str(message)
				try:
					type_, data = message.split("$")
					if(type_ == "message"):
						messageOutput = f"message${data}"
						GUI.incoming.insert(END, "")
						GUI.outgoing.insert(END, f"{data} << {self.username}")
					else:
						print(f"invalid type {type_}")
				except:
					messageList = []
					type_ = messageList[1]
					messageList.remove(type_)
					for part in messageList:
						messageOutput = f"{message}{part}"
				messageOutput = messageOutput.encode("utf-8")
				message_header = f"{len(messageOutput):<{HEADER_LENGTH}}".encode('utf-8')
				GUI.client_socket.send(message_header + messageOutput)
				GUI.incoming.insert(END, "")
				self.outgoing.insert(END, f"{messageOutput} << {self.username}")
			except:
				message = str(message)
				messageOutput = f"message${message}".encode("utf-8")
				message_header = f"{len(messageOutput):<{HEADER_LENGTH}}".encode("utf-8")
				self.client_socket.send(message_header + messageOutput)
				GUI.incoming.insert(END, "")
				GUI.outgoing.insert(END, f"{messageOutput} << {self.username}")

	def main(self):
		while True:
			try:

					username_header = self.client_socket.recv(HEADER_LENGTH)
					if(not len(username_header)):
						print("connection closed by server")
						sys.exit()
					print(username_header.decode("utf-8").strip())
					username_length = int(username_header.decode("utf-8").strip())

					username = self.client_socket.recv(username_lenght).decode("utf-8")

					message_header = self.client_socket.recv(HEADER_LENGTH)
					message_length = int(message_header.decode("utf-8").strip())
					messageRaw = self.client_socket.recv(message_length).decode("utf-8")

					type_, message = messageRaw.split("$")
			
					if(type_ == "message"):
						GUI.outgoing.insert(END, "")
						GUI.incoming.insert(END, f"{username} >> {message}")
					elif(type_ == "cmd"):
						if(username == "sever"):
							print("recieved server command")

			except IOError as e:
				if(e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK):
					print("READ ERR",str(e))
					sys.exit()
				continue

			# except Exception as e:
			# 	print(str(e))
			# 	sys.exit()		

def start(username):
	global connection
	connection = connectionHandler(username)
	global GUI
	GUI = mainWin(username)
	GUI.mainWindow.mainloop()

loginWin = inputNameWin()
