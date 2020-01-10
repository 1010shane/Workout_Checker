#!/usr/bin/python3
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

###CONSTANTS###
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class calBot:

	#p1 = Person("John", 36)
	#1.myfunc()

	"""
	Methods for handling things on the google calender side.
	calBots are made for each person using their name as the creds.
	"""
	def __init__(self, creds):
		self.creds = creds # credentials provided as a name, like "Ronnie"
		self.service = None # calender database 


	def createToken(self):
		"""
		Create a token for the user.
		This usually happens when there is no token present in the directory
		"""
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		# If there are no (valid) credentials available, let the user log in.
		creds = None
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
				userToken = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open(self.creds, 'wb') as token:
				pickle.dump(userToken, token)

		self.service = build('calendar', 'v3', credentials=userToken)

		
	def login(self):
		"""
		Logging into the calender using a token. 
		Token provided as "'username'.pickle"
		"""

		# convert creds, which is a name, to the 'token.pickle'
		if not self.creds:
			uesrToken = creds + '.pickle'

		# open the credentials file and set it to the object 
			if os.path.exists(userToken):
				with open(userToken, 'rb') as token:
					userToken = pickle.load(token)

		self.service = build('calendar', 'v3', credentials=userToken)


	def getEvents(self):
		"""
		Gets the scheduled swim, bike, run, or workout events in the calender for the day
		"""

		# 'Z' indicates UTC time
		# timezone is set according to time on local machine 
		now = datetime.datetime.now().isoformat() + 'Z' 

		# get up to 10 events for today and put it in a list
		events_result = self.service.events().list(calendarId='primary', timeMin=now,
											maxResults=10, singleEvents=True,
											orderBy='startTime').execute()
		events = events_result.get('items', [])

		# no events 
		if not events:
			print('No upcoming events found.')

		# filter through the events and sort out swim, bike, run, or workouts
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			print("Workouts for" + self.creds + "on" + now)
			print(start, event['summary'])


class stravaBot:
	"""
	Methods for handling things on the strava side
	"""
	def __init__(self, creds):
		self.creds = None


def main():
	test = calBot("Ronnie")
	test.createToken()

if __name__ == '__main__':
	main()
	