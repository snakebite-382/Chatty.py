# **Chatty.py**(_this title is a working title I'll come up with something better later on_)
A basic server using python sockets with a gui that is cabable of sending text, files, and links.

## **About** 
  ### **How it all started**
   I started this project after seeing a youtube video explaining the python module `sockets`. If you don't know what it is it     
   allows you to connect two computers together using python. Typically this works by having a host computer run the server script
   which manages all the connections. That is exactly how this works the server creates a socket that all the clients can connect 
   to and then when they send information it recieves, formats, and sends the information. I wanted to create a no hassle way to
   send documents, links, text, and files between my laptop and desktop while I'm working on things so I started this project
   
## **Requirements**
You must have the latest version of python installed and a text editor capable of editing python files.
   
## **Quickstart guide**
to get started quickly either download or clone the repository to your computer. If you download it unzip and extract all the 
files. Currently you have to set the ip address on the client script to the ip of the host. I'll change that when a GUI is added so 
you can input the IP you wish to connect to via the GUI. To do this open the python file labled `client.py` and find the line the 
reads `IP = ""` and between the two quotations type in the host ip. If you don't know the IP of the host computer just google how 
to find it for your specific operating system. You want your IPv4 address. Just find the address for whatever type of connection 
your going to have so if it's a local connection look for whichever address is listed as lan connection, etc. **_PLEASE NOTE THIS 
HAS NOT BEEN TESTED OUTSIDE OF A LOCAL CONNECTION ON THE SAME WIFI AND THIS MAY OR MAY NOt WORK OVER THE INTERNET PLEASE TELL ME 
IF YOU TEST THIS AND IT WORKS_**. Once you have edited the script simply run the `server.py` scritpt using either idle or the 
command  line if you don't know how just google it. Then run the `client.py` script and type a username into the text interface. 
You can connect as many clients as you want. To send a message just type it in and press enter. To load messages don't type 
anything just click enter (_this can't be avoided without a UI_). To quit stop the script

## **Known issues**
1) To put it simply the whole thing is broken because of how I'm attempting to send type information. This will be fixed shortly
2) You may have trouble connecting if you have a firewall up for the type of connection you are trying to establish. To fix this 
either edit or take down the firewall for that type of connection temporarily. If it helps this script sends a TCP connection 
overport 1234, this can be edited in the script if you know how to use the python sockets module`

## **Todo**
These are in no particular order and I may release them in any order 
- [x] Allow connections to be established between multiple clients and the server
- [X] Fix the issues with message sending
- [ ] Add a GUI
- [ ] Add a chat filter and prevent sending messages that are too long
- [ ] Test and fix long distance connections
- [ ] Allow for the sending of clickable links
- [ ] Allow for the sending of files
- [ ] Add server commands
- [ ] Allow for disconnection and reconnection
- [ ] Upgrade the GUI to something other than Tkinter
- [ ] Make it an application you can run like a normal program not just from the console
- [ ] Allow for you to change which port the server runs on
- [ ] Proper shuttdown not just closing the window and interupting the script
- [ ] Make customization easier

## **Customization**
* You can change the IP address to connect to and from in the client and server scripts respectively
* You can change the port in both client and server so you can run multiple servers. Please do research about what ports are open before changing anything
* If you understand the code you can change the way messages are displayed, and pretty much anything about this script just make sure that it all meshes up with the other script.
