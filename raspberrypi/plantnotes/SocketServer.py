# SocketServer.py
# Author: Jake Malley
# 27/05/14

# Creates new thread to listen on socket.

# Imports.
import threading, socket

exitFlag = 0
message_queue = [] 

class SocketThread(threading.Thread):
	def __init__(self, threadID, name, port):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name=name
		self.port=port

	def run(self):

		try:
			self.create_socket_server()
		except socket.error, e:
			print("Error creating socket: %s"%(e))

		else:

			try:
				while True:
					self.conn, self.addr = self.sock.accept()
					print("Connected to",self.addr)

					self.payload = self.conn.recv(32)
					self.message_received(self.payload) 

					self.conn.send(" msg_received")
						
			except socket.error, e:
				print("Socket Error:")
				print(e)
			finally:
				self.conn.close()
				self.sock.close()
				

		if exitFlag:
			thread.exit()

	def create_socket_server(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '127.0.0.1'
		print("HOST0")
		print(self.host)
		# Bind to that address + port.
		self.sock.bind((self.host, self.port))
		self.sock.listen(5) # Listen

	def message_received(self, payload):

		print("Received: %s" %(payload))
		if payload[:3] == "cmd":
			message_queue.append(payload)



x = SocketThread(1,"Socket",5559)
x.start()

        
