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
reads the measurements for a database and displays on an Adafruit
plate with an LCD display.
'''
# Program exits on push of "Select" button on the display board

# Dependences: mysql.connector and Adafruit_CarLCD
# See README for more explanation.

import mysql.connector

import time
import Adafruit_CharLCD as LCD


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
	lcd = LCD.Adafruit_CharLCDPlate()
	lcd.set_color(1.0,1.0,1.0)
	lcd.clear()
	lcd.home()
	lcd.set_backlight(1)
	return(lcd)

def clear_display(lcd):
	lcd.set_backlight(0)
	lcd.clear()

	

def display_data (lcd, t, h):
	temperture = str(t)
	humidity = str(h)
	lcd.clear()
	lcd.message("Temp = " + temperture + "\n" + "Humid = " + humidity )


def button_pressed(lcd):
	return (lcd.is_pressed(LCD.SELECT))

#===============================================

def main(args):
	lcd=set_up_display()
	finished=button_pressed(lcd)
	while not finished:
		try:
			data=read_current_temperature_humidity()
			idn, temperature, humidity = data[0]
			display_data(lcd, temperature, humidity)
			print(idn)
			for i in range (1,20):
				time.sleep(.5)
				finished=button_pressed(lcd)
				if finished:
					break
		except KeyboardInterrupt:
			lcd.clear()
			lcd.message("Keyboard\nInterrupt")
			time.sleep(5)
			lcd.clear()
			lcd.set_backlight(0)
			quit()
#		except (IOError,TypeError) as e:
#			print("Error: ", e)
#			quit()
	lcd.clear()
	lcd.set_backlight(False)
	
	return 0

#===============================================

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
