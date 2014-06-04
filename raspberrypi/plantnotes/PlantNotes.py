# PlantNotes.py
# Author: Jake Malley
# 27/05/14

# Listens on RF24 and Socket for data then adding it to the database.

# Imports
import SocketServer, RF24Listener, UpdateMySQL # Our Files
import sys, time

port = int(raw_input("Enter port> ")) # For testing only, actual service will run on port 5021
server = SocketServer.SocketThread(1, "SocketThread", port)
radio_listener = RF24Listener.RF24ListenerThread(2, "ListenThread")

# Start both threads.
server.start()
radio_listener.start()


	
try:
	while True:
		# Deal with socket messages
		if SocketServer.message_queue:
			# Get + remove message
			socket_message = SocketServer.message_queue[0]
			SocketServer.message_queue.remove(socket_message)
			# Add the message to thr writing queue
			RF24Listener.writing_queue.append(socket_message)

		# Deal with RF24 Messages
		if RF24Listener.message_queue:
			# Get + remove message
			rf24_message = RF24Listener.message_queue[0]
			RF24Listener.message_queue.remove(rf24_message)
			# Make a new thread to input this to SQL
			sql_thread = UpdateMySQL.InputData(3, "SQLThread",rf24_message)
			sql_thread.start()

except KeyboardInterrupt:

	# Close the threads
	server.stop_thread()
	radio_listener.stop_thread()

	print("Exiting")
	


time.sleep(0.5)





