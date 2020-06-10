import socket # for connecting
import errno # for error handling
import sys # for quiting the program
import threading # to run multiple loops
from tkinter import * # for the gui
import time # for time waits


HEADER_LENGTH = 10 # the length of headers

IP = ""
PORT = 1234 # what port to connect to 
validTypes = ["message"] # the valid types that can be sent

class inputNameWin():
	def __init__(self):
		#create the window
		self.window = Tk()
		self.window.title("login")

		# create the input label
		self.inputLabel = Label(self.window, text="Type in your username, then click connect")
		self.inputLabel.grid(row=0, column=1)

		# create the input box
		self.inputName = Entry(self.window, width="10")
		self.inputName.grid(row=1, column=0, columnspan=2)

		# create the button to connect using the inputted data
		self.connectButton = Button(self.window, text="CONNECT", command= lambda : self.checkName(self.inputName.get()))
		self.connectButton.grid(row=2, column=0, columnspan=2)
		self.window.mainloop()

	def checkName(self, name):
		name = name.strip()
		# check if the name is legit if so start the program
		if len(name) <= 3 :
			self.inputLabel['text'] = f"Username {name} is too short! Try another"
		elif len(name) >= 15:
			self.inputLabel['text'] = f"Username {name} is too long! Try another"
		elif name.lower() == "server":
			self.inputLabel['text'] = f"Illegal username : {name}"
		else:
			self.window.destroy()
			start(name)


class mainWin():
	def __init__(self, username):
		# set the username as a variable
		self.username = username
		# create the main window
		self.mainWindow = Tk()
		self.mainWindow.title(f"Chatty.py client [NO CONNECTION] NAME = {self.username}")
		self.mainWindow.configure(bg="white")

		self.padSizeX = 5
		self.padSizeY = 60

		# create the status bar
		self.status = Label(self.mainWindow, text=f"Username : {self.username} [NO CONNECTION]", fg="black", bg="white")
		self.status.grid(row=0, column=0, columnspan=2)

		# create the input box and button
		self.messagEntry = Entry(self.mainWindow, fg="black", bg="white", width=60)
		self.messageSend = Button(self.mainWindow, text="Send", command= lambda : connection.sendMessage(self.messagEntry.get()), fg="green", bg="white", activebackground="white", activeforeground="black")
		self.messagEntry.grid(row=2, column=0, columnspan=2)
		self.messageSend.grid(row=3, column=0, columnspan=2)

		# create the incoming messages list
		self.incoming = Listbox(self.mainWindow, fg="green", bg="white", width=50, height=25, selectbackground="blue", highlightcolor="green2")
		self.incoming.grid(row=1, column=0)

		# create the outgoing messages list box
		self.outgoing = Listbox(self.mainWindow, fg="blue", bg="white", width=50, height=25, selectbackground="green", highlightcolor="green2")
		self.outgoing.grid(row=1, column=1)

class connectionHandler():
	def __init__(self, username):
		# create the socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((IP, PORT))
		self.client_socket.setblocking(False)

		# join the server
		self.username = username.encode("utf-8");
		self.username_header = f'{len(username):<{HEADER_LENGTH}}'
		self.username_header = self.username_header.encode('utf-8')

		self.client_socket.send(self.username_header + self.username)

		self.username = username

		# create the main loop thread
		main = threading.Thread(target=self.main)
		main.start()
		# create a status update loop
		updateLoop = threading.Thread(target=self.updateStatus)
		updateLoop.start()

	def updateStatus(self):
		time.sleep(2) # wait a bit so that everything is properly connected
		while True:
			name = self.username
			GUI.status['text'] = f"[CONNECTED] Username : {name} My IP : {socket.gethostbyname(socket.gethostname())} SERVER IP : {IP} ON PORT : {PORT}"

	def sendMessage(self,message):
		message = str(message)
		# first see if the user is using $ in the message and if it's to send type data
		try:
			type_, data = message.split("$", 1) # split the data
			if(type_ in validTypes): # if they inputted a valid type
				messageOutput = f"{type_}${data}".encode('utf-8')
				header = f"{len(messageOutput):< {HEADER_LENGTH}}".encode('utf')
				self.client_socket.send(header + messageOutput)

				GUI.incoming.insert(END, '')
				GUI.outgoing.insert(END, f'{data} << {self.username}')

			else: # if they didn'y
				messageOutput = f"message${message}".encode("utf-8")
				header = f"{len(messageOutput):< {HEADER_LENGTH}}".encode('utf')
				self.client_socket.send(header + messageOutput)

				GUI.incoming.insert(END, '')
				GUI.outgoing.insert(END, f'{message} << {self.username}')
		except:
			# if all else fails just send the message
			messageOutput = f"message${message}".encode('utf-8')
			header = f"{len(messageOutput):< {HEADER_LENGTH}}".encode('utf')
			self.client_socket.send(header + messageOutput)

			GUI.incoming.insert(END, '')
			GUI.outgoing.insert(END, f'{message} << {self.username}')



	def main(self):
		while True:
			# try to recieve data
			try:
				# revieve the package data
				username_header = self.client_socket.recv(HEADER_LENGTH)
				if(not len(username_header)):
					print("connection closed by server")
					sys.exit()
				username_length = int(username_header.decode("utf-8").strip())

				username = self.client_socket.recv(username_length).decode("utf-8")

				message_header = self.client_socket.recv(HEADER_LENGTH)
				message_length = int(message_header.decode("utf-8").strip())
				messageRaw = self.client_socket.recv(message_length).decode("utf-8")

				type_, message = messageRaw.split("$",)
		
				# handle different packet types
				if(type_ == "message"):
					GUI.outgoing.insert(END, "")
					GUI.incoming.insert(END, f"{username} >> {message}")
				elif(type_ == "cmd"):
					if(username == "server"):
						print("recieved server command")
						GUI.outgoing.insert(END, "")
						GUI.incoming.insert(END, f"[{username.upper()}] >> {message}")
			# do some error handling
			except IOError as e:
				if(e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK):
					print("READ ERR",str(e))
					sys.exit()
				continue	
# start the actual program
def start(username):
	global connection
	connection = connectionHandler(username)
	global GUI
	GUI = mainWin(username)
	GUI.mainWindow.mainloop()

loginWin = inputNameWin()
