# UpdateMySQL.py
# Author: Jake Malley
# 27/05/14

# Updates SQL data dependant on input

# Imports
import threading, MySQLdb, time

exitFlag = 0

class InputData(threading.Thread):
	def __init__(self, threadID, name, input_string):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.input_string = input_string

	def run(self):
		# Firstly sub string the data.
		sensor_name = self.input_string[:4]
		sensor_data = self.input_string[4:]

		# Connect to the database with user root and password root123
		con = MySQLdb.connect(host="localhost",user="root",passwd="root123", db="sensors_db")
		cursor = con.cursor()

		# Check if row exists
		q = "SELECT count(1) from tbl_sensors where sensor_name='"+sensor_name+"';"
		cursor.execute(q)

		if cursor.fetchone()[0]:

			# Update the the table if there is already a sensor witht that sensor_name
			q = "UPDATE tbl_sensors SET sensor_data="+sensor_data+" WHERE sensor_name='"+sensor_name+"';"
			cursor.execute(q)

		else:
			# Create a new row for that sensor
			q = "INSERT INTO tbl_sensors (sensor_name, sensor_data) VALUES ('"+sensor_name+"', "+sensor_data+");"
			cursor.execute(q)

		# Log Data 
		now = str(time.ctime())
		q = "INSERT INTO tbl_datalog (now, sensor_name, sensor_data) VALUES ('"+now+"','"+sensor_name+"', "+sensor_data+");"
		cursor.execute(q)       
		print("SQL Done")

		if exitFlag:
			thread.exit()

