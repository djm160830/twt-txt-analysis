# NAME:         Darla Maneja
# EMAIL:        djm160830@utdallas.edu
# SECTION:      CS4372.001
# Assignment 5

# Getting model
import os
import spacy
from dotenv import load_dotenv

# Getting tweets + preprocessing
import twitter
import re

# Real-time graph updating
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
import time

# Debugging
import inspect
import pdb

# Get recognizer
nlp = spacy.load("en_core_web_sm")
project_folder = os.getcwd()  # Get current directory
load_dotenv(os.path.join(project_folder, '.env')) # Read from .env

# Twitter API
API_KEY=os.getenv('API_KEY')
API_KEY_SECRET=os.getenv('API_KEY_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')
# Stream filter parameters
# USERS=['@twitter']
# Dallas, Houston, San Francisco, New York
COORDINATES=["-97.94311523437501,32.31499127724556,-96.470947265625,33.04550781490999,\
				-95.71289062500001,29.46829664171322,-95.05371093750001,30.050076521698735,\
				-118.56445312500001,33.58716733904659,-117.69653320312501,34.243594729697406,\
				-121.88232421875001,38.19502155795575,-121.11328125000001,38.90813299596705,\
				-122.87109375000001,47.18971246448421,-121.88232421875001,47.65058757118736,\
				-74.54772949218751,40.35282369083777,-72.97668457031251,41.529141988723104"] # long-lat, long-lat
LANGUAGES=['en']    


def listener():
	return twitter.Api(
		consumer_key=API_KEY,
		consumer_secret=API_KEY_SECRET,
		access_token_key=ACCESS_TOKEN,
		access_token_secret=ACCESS_TOKEN_SECRET)


# Plot
fig = plt.figure()
fig.set_size_inches((11,5))
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []

thing = dict()

api = listener()
class TwtTxtAnalysis():

	def __init__(self):
		# Plot data and read tweets at the same time
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete(self.animate())
		finally:
			loop.run_until_complete(
				loop.shutdown_asyncgens())
			loop.close()
			plt.show() # Keep plot window open

	async def read_tweets(self):
		# Get a filtered view of public statuses
		timeout = time.time()+30
		for line in api.GetStreamFilter(locations=COORDINATES, languages=LANGUAGES): # I REMOVED track=USERS
			if time.time()>timeout: break
			else:
				raw = line['extended_tweet']['full_text'] if 'extended_tweet' in line else line['text']
				# Set up doc
				# Helps recognize location-type entities
				txt = re.sub('@\s', 
					"at ", 
					raw, 
					flags=re.IGNORECASE) 
				# Remove hashtags and @ | removed [\u263a-\U0001f645] , \u00A0-\U0001FADF
				txt1 = re.sub('#[a-zA-Z0-9]+\w?|@|(&amp)+;?|[\u2020-\U0001FADF]+', 
					"", 
					txt)
				# Remove website links [^\\u0000-\\u007F]
				txt2 = re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])+', 
					"", 
					txt1, 
					flags=re.IGNORECASE)
				# Helps 'PERSON' recognition. MichelleObama (not recognized) -> Michelle Obama (Recognized)
				clean = re.compile(r'([a-z])([A-Z])')
				txt3 = re.sub(clean, 
					r'\1 \2', 
					txt2)
				doc = nlp(txt3)

				await asyncio.sleep(.4)
				if doc.ents:
					# if raw!=doc: print(f'==RAW: {raw}')
					# if txt!=raw: print(f'	0=INTERMEDIATE: {txt}')
					# if txt1!=txt: print(f'	1=INTERMEDIATE: {txt1}') 
					# if txt2!=txt1: print(f'	2=INTERMEDIATE: {txt2}') 
					# if txt3!=txt2: print(f'	3=INTERMEDIATE: {txt3}') 
					print(f'==RES: {doc}')
					yield [(X.text, X.label_) for X in doc.ents]
				else:
					continue

	async def animate(self):
		ax1.clear()
		plt.xlabel('Entity')
		plt.ylabel('Count')
		plt.title('Live graph with matplotlib')

		# Get updated dictionary
		async for entities in self.read_tweets():
			print(f'==ENT: {entities}\n\n')
			for _, e in entities:
				if e not in thing: 
					thing[e]=1
				else:
					thing[e]+=1
			ax1.bar(list(thing.keys()), list(thing.values()), color='blue')
			plt.pause(0.01)

if __name__ == "__main__":
	TwtTxtAnalysis()
