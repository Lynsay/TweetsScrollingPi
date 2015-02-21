#LCD Scrolling Tweets

Lynsay A. Shepherd, February 2015

##Overview

This is a Python script which allows you to scroll your Twitter feed across a 16x2 LCD screen connected to the GPIO of a Raspberry Pi.

The script requires the use of several libraries.  The Adafruit_CharLCDPlate library- https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_CharLCDPlate and the Twython pure Python wrapper for the Twitter API- https://github.com/ryanmcgrath/twython

This script was originally written for the <a href="http://www.adafruit.com/product/1110">Adafruit RGB Negative 16x2 LCD+Keypad Kit for the Raspberry Pi</a>.  This LCD screen can turn a number of colours.  The screen will turn blue when a tweet is received, purple if a user receives an @ mention, and red if there's an error.
