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
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
# Los Angeles, San Francisco, rural CA, Dallas, Houston, rural TX, rural&urban NY, Boston, rural MA
COORDINATES = ["-118.55895996093751,33.64663552343716,-117.42187500000001,34.34343606848294,\
				-122.49481201171876,37.182202221079805,-121.84661865234376,37.85967565921003,\
				-118.1689453125,35.137879119634185,-116.26831054687501,36.02244668175846,\
				-97.71240234375001,32.38923910985902,-96.405029296875,33.02708758002874,\
				-95.70190429687501,29.46829664171322,-95.00976562500001,29.954934549656144,\
				-102.32116699218751,30.963479049959364,-100.96984863281251,31.737511125687828,\
				-74.64660644531251,42.29762739128458,-74.10552978515626,42.56926437219384,\
				-74.67407226562501,40.43022363450862,-73.30078125000001,41.12074559016745,\
				-71.20788574218751,42.18782901059085,-70.88653564453126,42.48830197960227,\
				-72.86819458007814,42.525760129656845,-72.65602111816408,42.71927257380149"] # long-lat, long-lat
LANGUAGES = ['en']    

# Return twitter listener
def listener():
	return twitter.Api(
		consumer_key=API_KEY,
		consumer_secret=API_KEY_SECRET,
		access_token_key=ACCESS_TOKEN,
		access_token_secret=ACCESS_TOKEN_SECRET)


# Reads tweets in real time from twitter, and outputs entity counts as a pyplot graph
class TwtTxtAnalysis():
	def __init__(self):
		# Plot
		self.fig = plt.figure()
		self.fig.set_size_inches((11,5))
		self.ax = self.fig.add_subplot(1,1,1)
		# Tweet, entity vars
		self.api = listener()
		self.doc = None
		self.d = dict()
		
		# Plot data and read tweets at the same time
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete(self.animate())
		finally:
			loop.run_until_complete(
				loop.shutdown_asyncgens())
			loop.close()
			plt.show() # Keep plot window open

	# Prepare tweets to be accurately analyzed by nlp
	async def clean_tweets(self, raw):
		# Helps nlp recognize location-type entities
		txt = re.sub('@\s', 
			"at ", 
			raw, 
			flags=re.IGNORECASE) 
		# Remove #, @, and emojis
		txt1 = re.sub('#[a-zA-Z0-9]+\w?|@|(&amp)+;?|[\u2020-\U0001FADF]+', 
			"", 
			txt)
		# Remove website links 
		txt2 = re.sub('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])+', 
			"", 
			txt1, 
			flags=re.IGNORECASE)
		# Helps nlp with 'PERSON' recognition. ex) MichelleObama (not recognized) -> Michelle Obama (Recognized)
		clean = re.compile(r'([a-z])([A-Z])')
		txt3 = re.sub(clean, 
			r'\1 \2', 
			txt2)

		self.doc = txt3

	# Yields list of entities from tweets to graph animator
	async def read_tweets(self):
		# Get a filtered view of public statuses
		timeout = time.time()+30
		for i, line in enumerate(self.api.GetStreamFilter(locations=COORDINATES, languages=LANGUAGES)): 
			if time.time()>timeout: break
			else:
				raw_tweet = line['extended_tweet']['full_text'] if 'extended_tweet' in line else line['text']
				await self.clean_tweets(raw_tweet)
	
				doc = nlp(self.doc)

				if doc.ents:
					print(f'{i}==RAW: {raw_tweet}')
					yield [(X.text, X.label_) for X in doc.ents]
				else:
					continue

	# Draw bar graph using recognized entities
	async def animate(self):
		self.ax.clear()
		plt.xlabel('Entity')
		plt.ylabel('Count')
		plt.title('Live graph with matplotlib')

		# Get updated dictionary
		async for entities in self.read_tweets():
			print(f'==ENT: {entities}\n\n')
			# Increment entity count
			for _, e in entities:
				if e not in self.d: 
					self.d[e] = 1
				else:
					self.d[e] += 1
			self.ax.bar(list(self.d.keys()), list(self.d.values()), color='blue')
			plt.pause(0.01)

if __name__ == "__main__":
	TwtTxtAnalysis()
