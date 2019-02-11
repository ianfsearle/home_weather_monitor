#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  read_env.py
#  
#  Copyright 2018  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
'''
This is a part of a two progam set which will run on two Raspberry Pis.
One Pi uses a DHT22 sensor to read the temperature and humidity and
to write the measurements into a database.  The other (this one)
reads the measurements for a database and displays on an Grove Pi LCD
display.
'''

# Dependences: mysql.connector and GrovePi LCD Display
# See README for more explanation.

import mysql.connector

import time
from grovepi import *
from grove_rgb_lcd import *


# Constants
HOST="192.168.1.113" # Change to suit address of sensor Raspberry Pi
USER="inte2043"
PASSWORD="Business_IT"
DATABASE="inte2043"
QUERY="SELECT id, temperature, humidity FROM environment WHERE record_timedate = (SELECT MAX(record_timedate) FROM environment);"
		

def create_mysql_connection():
	mydb = mysql.connector.connect (
	host=HOST,
	user=USER,
	passwd=PASSWORD,
	database=DATABASE)
	return(mydb)

def read_current_temperature_humidity():
	conn=create_mysql_connection()
	curr=conn.cursor()
	curr.execute(QUERY)
	result=curr.fetchall()
	curr.close()
	conn.close()
	return (result)

def set_up_display():
	setRGB(0,255,0)
	setText(" ")
	return(0)

def display_data (t, h):
	temperture = str(t)
	humidity = str (h)
	setText("Temp = " + temperture + "\n" + "Humid = " + humidity )

def clear_display ():
	setRGB(0,0,0)
	setText(" ")


#def button_pressed(lcd):
#	return (lcd.is_pressed(LCD.SELECT))

#===============================================

def main(args):
#	envdb=create_mysql_connection()
	lcd=set_up_display()
	finished=False  #button_pressed(lcd)
	while not finished:
		try:
			data=read_current_temperature_humidity()
			idn, temperature, humidity = data[0]
			display_data(temperature, humidity)
			time.sleep(60)
		except KeyboardInterrupt:
			setText("Keyboard\nInterrupt")
			time.sleep(5)
			clear_display()
			quit()
		except (IOError,TypeError) as e:
			print("Error: ", e)
			time.sleep(10)
#			quit()
	clear_display()
	
	return 0

#===============================================

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
