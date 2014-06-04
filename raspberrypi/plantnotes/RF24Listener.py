# RF24Listener.py
# Author: Jake Malley
# 27/05/14

# RF24 listening class.

# Imports
from pyRF24 import pyRF24
import threading, time

exitFlag = 0
message_queue = []
writing_queue = []

class RF24ListenerThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True

		# Setup Radio
		self.pipes = [0xF0F0F0F0E1, 0xF0F0F0F0E2]
		self.radio  = pyRF24("/dev/spidev0.0", 8000000, 18, retries = (15, 15), channel = 76,
			dynamicPayloads = True, autoAck = True)
		self.radio.openWritingPipe(self.pipes[0])
		self.radio.openReadingPipe(1, self.pipes[1])
		self.reading_channel = 76
		self.writing_channel = 78
		self.radio.printDetails()

	def run(self):

		self.radio.startListening()
		self.radio.setChannel(self.reading_channel)

		while self.running:

			self.payload = []

			# Do we need to write anything?
			self.check_writing_queue()

			if self.radio.available():

				# Make sure we clear the payload
				del self.payload[:]
				# Get payload size
				length = self.radio.getDynamicPayloadSize()

				# Read Payload
				self.payload = self.radio.read(length)[:length]

				self.message_received(self.payload)

		if exitFlag:
			thread.exit()

	def message_received(self, payload):

		print("Radio Received: %s" %(payload))
		message_queue.append(payload)

	def check_writing_queue(self):

		if writing_queue:
			self.radio.stopListening()
			self.radio.setChannel(self.writing_channel)

			time.sleep(0.25)

			# Get what we want to write and remove it from queue.
			write_payload = writing_queue[0]
			writing_queue.remove(write_payload)

			self.radio.write(write_payload)
			print("Radio Sent: %s"%(write_payload))

			time.sleep(0.25)
			self.radio.startListening()
			self.radio.setChannel(self.reading_channel)

	def stop_thread(self):

		self.running = False

