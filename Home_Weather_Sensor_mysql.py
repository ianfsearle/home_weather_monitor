#!/usr/bin/python3
'''
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.


This version writes data to a MySQL database.  See connection details in constants definitions below.
'''
import Adafruit_DHT
from time import sleep, time
import mysql.connector

#=====================================
# Constants

# Flage to tell is DB is being used
DB_WRITE=True

# Tell the program how many seconds in a minute
SECONDS_IN_MINUTES=60
# Set the interval between writes to the dabase in minutes
MINUTES_TO_WAIT_BETWEEN_DB_WRITES = 10
#Write to the database every "db_write_period" seconds
db_write_period = SECONDS_IN_MINUTES*MINUTES_TO_WAIT_BETWEEN_DB_WRITES

# Identify the type of sensor to be used.
sensor = Adafruit_DHT.DHT22
# Identify the GPIO port being used
pin = 4

# Set constants according to the environment in which the program is to run
HOSTNAME='localhost'
USERNAME='inte2043'
PASSWD='Business_IT'
DBNAME='inte2043'
TABLENAME='environment'

#=====================================
# Function Definitions

def main():

	def set_query (temp, hum):
		t = str(temp)
		h = str(hum)
		return ("INSERT INTO " + TABLENAME + "(temperature, humidity) VALUES ("+t+","+h+");")
		
	def _sql_write(sql_query):
		db=mysql.connector.connect(host=HOSTNAME,user=USERNAME,passwd=PASSWD,db=DBNAME)
		curs = db.cursor()
		curs.execute(sql_query)
		db.commit()
		curs.close()
		db.close()
		return (0)

	def sql_write(sql_query):
		if DB_WRITE:
			_sql_write(sql_query)
	
	def _write_data (temp, hum):
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
		return(0)

	def write_data (temp,hum):
		if temp is not None and hum is not None:
			_write_data (temp, hum)
			return(0)
		else:
			print('Failed to get reading. Try again!')
			return(1)

	def read_sensor (sensor, pin):
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		return Adafruit_DHT.read_retry(sensor, pin)

#=====================================

# Main program starts here
   
	starttime=time()

	hum, temp = read_sensor(sensor, pin)
	sleep(.05)
	sql_write(set_query (temp, hum))
	write_data(temp, hum)

	while True:
		try:
			hum, temp = read_sensor(sensor, pin)
			elapsedtime=time()
			if elapsedtime-starttime >= db_write_period:
				sql_write(set_query(temp,hum))
				write_data(temp,hum)
				starttime=time()
			sleep(10)
		except KeyboardInterrupt:
			print("\nKeyboard Interrupt")
			sleep(5)
			quit()
		except (IOError,TypeError) as e:
			print("Error: ", e)
            
if __name__ == "__main__":
	main()
