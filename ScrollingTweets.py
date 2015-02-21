#Scroll your Twitter feed on an LCD screen connected to the GPIO of a Raspberry Pi
#Requires several libraries...
#The Adafruit_CharLCDPlate library- https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_CharLCDPlate
#The Twython pure Python wrapper for the Twitter API- https://github.com/ryanmcgrath/twython

#Version 1.0 December 2013
#Version 2.1 December 2014
#Version 2.2 February 2015

#Written by Lynsay A. Shepherd

#import stuff
from twython import Twython
from twython import TwythonStreamer
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import sys
import urllib2
import time

# Initialize the LCD plate
lcd = Adafruit_CharLCDPlate(busnum=1)


#authenticate with Twitter
#Twitter developer site to get the required values for your account
APP_KEY=''
APP_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''

#connect via Twython
twitter=Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter.verify_credentials()
class MyStreamer(TwythonStreamer):

	#Retrieve the Twitter data stream
    def on_success(self, data):
    	
        if 'text' in data:
        	try:
        		#get the username of the person who sent the tweet and the content
        		tweetFromUserName=data['user']['screen_name']+': '.encode('ascii','replace')
        		tweetContent=data['text'].encode('ascii','replace')
        		tweetContent=tweetContent.lower()
        		myUsername = "@add_user_name_here"
        		
        		#call the function to prepare the data for the LCD screen
        		self.displayData(tweetFromUserName,tweetContent, myUsername)
        		
        	except:
        		errorDetails="Issue retrieving data"
        		self.data_error(errorDetails)
        		
        		

    def displayData(self, tweetFromUserName,tweetContent, myUsername ):
		#if the tweet is an @reply
		#space added to myUsername so it only returns data for @add_user_name_here 
		#i.e. excludes replies that have @add_user_name_here as part of the username for example @add_user_name_hereeeeee
		if myUsername+" " in tweetContent:
			lcd.clear()
			lcd.backlight(lcd.VIOLET)
			#get tweet content but remove my username from the tweet
			tweetContent=tweetContent.replace('@add_user_name_here','')
			#get tweet length- needed to decide how to display it
			tweetContentLength=len(tweetContent)
			
			if tweetContentLength <16:
				self.display_tweet_lcd(tweetFromUserName, tweetContent)
				
			else:
				self.scroll_tweet_lcd(tweetFromUserName, tweetContent, tweetContentLength)
					
		#else its just a regular tweet in my timeline
		else:
			lcd.clear()
			lcd.backlight(lcd.ON)
			tweetContentLength=len(tweetContent)
			if tweetContentLength <16:
				self.display_tweet_lcd(tweetFromUserName, tweetContent)
					
			else:
				self.scroll_tweet_lcd(tweetFromUserName, tweetContent, tweetContentLength)
    
    
    
    #dataerror function
    def data_error(self, errorDetails):
    	lcd.clear()
    	lcd.backlight(lcd.RED)
    	errorContentLength=len(errorDetails)
    	
    	if errorContentLength <16:
    		self.display_tweet_lcd("ERROR:", errorDetails)
    		
    	else:
    		self.scroll_tweet_lcd("ERROR:", errorDetails, errorContentLength)
    	
    	
    	
    #display >16 chars
    def scroll_tweet_lcd(self, tweetFromUserName, tweetContent, tweetContentLength):
    	#loop through chars
		x = 0
		y=15
		while x < tweetContentLength+1:
			tweetContentPart = tweetContent[x:y]
			lcd.message(tweetFromUserName+"\n"+tweetContentPart)
			sleep(.25)
			x+=1
			y+=1
			lcd.clear()	
    
    
    
    #display <16 chars
    def display_tweet_lcd(self, tweetFromUserName, tweetContent):
		lcd.message(tweetFromUserName+"\n"+tweetContent)
		
    #twython error- error getting data from Twitter itself  
    def on_error(self, status_code, data):
    	errorDetails="Twitter issue- check service status"
    	self.data_error(errorDetails)
    	
class netConnection():
	#check internet connection
	def check_connection(self):
		try:
			urllib2.urlopen("http://www.google.com").close()
			print "Internet Connected"
			return True
		except urllib2.URLError:
			print "No internet connection"
			return False

#check connection, start the stream
	def start_program(self):
		isConnected=self.check_connection()
		if isConnected ==True:
			# authenticate my stream
			stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
			stream.user(screen_name="add_user_name_here")
		else:
			stream.disconnect()
			lcd.clear()	
			lcd.message("no connection!")
			time.sleep(60)
			self.start_program()
			
startup=netConnection()
startup.start_program()
