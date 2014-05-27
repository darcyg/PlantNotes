# PlantNotes.py
# Author: Jake Malley
# 27/05/14

# Listens on RF24 and Socket for data then adding it to the database.

# Imports
import SocketServer, RF24Listener # Our Files
import sys, time

p = int(raw_input("Enter port> "))
server = SocketServer.SocketThread(1, "SocketThread", p)
server.start()

radio_listener = RF24Listener.RF24ListenerThread(2, "ListenThread")
radio_listener.start()

while True:
	
	# Deal with socket messages
	if SocketServer.message_queue:
		# Get + remove message
		socket_message = SocketServer.message_queue[0]
		SocketServer.message_queue.remove(socket_message)
		# Add the message to thr writing queue
		RF24Listener.writing_queue.append(socket_message)
		

	time.sleep(0.5)





