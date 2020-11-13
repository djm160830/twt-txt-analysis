# NAME:         Darla Maneja
# EMAIL:        djm160830@utdallas.edu
# SECTION:      CS4372.001
# Assignment 5

import pdb
import twitter
import os
from dotenv import load_dotenv

# DELETE IF USING SPACY
# import nltk
# from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re

import spacy
# import en_core_web_sm

# Real-time graph updating
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
import time

# Debugging
import inspect

# DELETE IF USING SPACY
# Set java.exe location
# os.environ['JAVAHOME'] = "C:\\Program Files\\Java\\jdk-13.0.1\\bin\\java.exe"
nlp = spacy.load("en_core_web_sm")
# nlp = en_core_web_sm.load()

project_folder = os.getcwd()  # Get current directory
load_dotenv(os.path.join(project_folder, '.env')) # Read from .env

# Twitter API
API_KEY=os.getenv('API_KEY')
API_KEY_SECRET=os.getenv('API_KEY_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')
# Stream filter parameters
# USERS=['@twitter']
# COORDINATES='32.77,-96.79'
# COORDINATES=["-122.75,36.8,-121.75,37.8,-74,40,-73,41"]
# COORDINATES=["-98.49243164062501,29.38217507514529,-96.80053710937501,32.8149783969858"] # long-lat,long-lat
# Dallas, Houston, San Francisco, New York
COORDINATES=["-97.94311523437501,32.31499127724556,-96.470947265625,33.04550781490999,\
				-95.71289062500001,29.46829664171322,-95.05371093750001,30.050076521698735,\
				-118.56445312500001,33.58716733904659,-117.69653320312501,34.243594729697406,\
				-121.88232421875001,38.19502155795575,-121.11328125000001,38.90813299596705,\
				-122.87109375000001,47.18971246448421,-121.88232421875001,47.65058757118736,\
				-74.54772949218751,40.35282369083777,-72.97668457031251,41.529141988723104"]
LANGUAGES=['en']    
# Stanford NER Tagger
CLASSIFIER=os.path.join(project_folder, 'stanford-ner-4.0.0\\stanford-ner-4.0.0\\classifiers\\english.all.3class.distsim.crf.ser.gz')
JAR_FILE=os.path.join(project_folder, 'stanford-ner-4.0.0\\stanford-ner-4.0.0\\stanford-ner.jar')


def listener():
	return twitter.Api(
		consumer_key=API_KEY,
		consumer_secret=API_KEY_SECRET,
		access_token_key=ACCESS_TOKEN,
		access_token_secret=ACCESS_TOKEN_SECRET)

fig = plt.figure()
fig.set_size_inches((11, 5))
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []

# thing = [(1,2), (2,3), (3,6), (4,9), (5,4), (6,7), (7,7), (8,4), (9,3), (10,7)]
thing = {"PERSON": 2, "NORP": 4, "FAC": 2, "ORG":1}
# it = iter(thing)

"""ASYNC IDEA
async def async_generator():
	for i in range(3):
		if "ORG" in thing:
			yield thing["ORG"]+=1
"""

# def animate was here above TxtTxtAnalysis

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
			# ani = animation.FuncAnimation(fig, self.animate, fargs=[thing], interval=1000) # fargs=[it] works | took out fargs=[thing]
			loop.close()
			plt.show() # Keep plot window open


	async def read_tweets(self):
		# Get a filtered view of public statuses
		# NOTE: check if there is a line['extended_tweet']['full_text'] before line['text']
		timeout = time.time()+20
		for line in api.GetStreamFilter(locations=COORDINATES, languages=LANGUAGES): # I REMOVED track=USERS
			if time.time()>timeout: break
			else:
				raw = line['extended_tweet']['full_text'] if 'extended_tweet' in line else line['text']
				# Set up doc
				# txt = raw.lower() 
				# COPY EVERYTHING BELOW INTO HERE, FIGURE OUT A WAY TO PRINT COUNTS AND STUFF IN REAL TIME
				txt = re.sub("@\s", "at ", raw, flags=re.IGNORECASE)
				txt = re.sub("([a-z])([A-Z])" r'\1 \2', txt) # THIS CAUSES ERORR. I JUST WANT TO PUT A SPACE BETWEEN
				# THE TWO MATCHED ITEMS SO STUFF LIKE MichelleObama TURNS INTO Michelle Obama AND THE ENTITY RECOGNIZTER 
				# RECOGNIZES IT AS A PERSON INSTEAD OF AN ORGANIZATION.
				#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ START HERE DONT RUN ANYTHING BC THERES ERROR AS A RESULT
				txt = re.sub("@+|#+|((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])+|[^\\u0000-\\u007F]+|(&amp)+", "", txt, flags=re.IGNORECASE)
				# txt = re.sub("(@(\w){1,15}(?!\w))","",txt)
				# txt = re.sub("[^a-z0-9\s]","",txt)
				doc = nlp(txt)

				await asyncio.sleep(.4)
				if doc.ents:
					print(f'==RAW: {raw}')
					print(f'==RES: {doc}')
					yield [(X.text, X.label_) for X in doc.ents]
				else:
					continue

				# Check if doc.ents is a list so you can do the next line correctly
				# print(f'This should be the text and then label: {}, {}')
				# DON'T RUN ANYTHIG YET FINISH OPERATIONS IN HERE


		# txt=line['text']
		# tt=txt.lower()
		# ttt=re.sub("(@(\w){1,15}(?!\w))","",tt)
		# tttt=re.sub("[^a-z0-9\s]","",ttt)
		# doc=nlp(tttt)
		# [(X.text,X.label_) for X in doc.ents]


	# async def animate(self, i, itr):
	async def animate(self):
		# x,y=next(itr)
		# x=next(itr)

		# print(f'i: {i}, x: {x}, y: {y}')
		ax1.clear()

		# x,y = thing[1]

		# print(f'xs: {xs}, ys: {ys}')
		# xs.append(float(x))
		# ys.append(float(y))
	   
		# ax1.plot(xs, ys)
		# ax1.bar(list(itr.keys()), list(itr.values()))

		plt.xlabel('Entity')
		plt.ylabel('Count')
		plt.title('Live graph with matplotlib')

		# Get updated dictionary
		async for entities in self.read_tweets():
			print(f'entities: {entities}\n')
			for _, e in entities:
				if e not in thing: 
					thing[e]=1
				else:
					thing[e]+=1
			ax1.bar(list(thing.keys()), list(thing.values()), color='blue')
			plt.pause(0.01)
			# pdb.set_trace()



if __name__ == "__main__":
	TwtTxtAnalysis()
	# Set up a listener
	# api = listener() 


	# ani = animation.FuncAnimation(fig, animate, fargs=[it], interval=1000) # fargs=[it] works
	# plt.show()

	# pdb.set_trace()

"""
	pdb.set_trace()


	# Get a filtered view of public statuses
	# NOTE: check if there is a line['extended_tweet']['full_text'] before line['text']
	for i, line in enumerate(api.GetStreamFilter(locations=COORDINATES, languages=LANGUAGES)): # I REMOVED track=USERS
		if i==5: break
		else:
			txt = line['extended_tweet']['full_text'] if 'extended_tweet' in line else line['text']
			# Set up doc
			txt = txt.lower()
			# COPY EVERYTHING BELOW INTO HERE, FIGURE OUT A WAY TO PRINT COUNTS AND STUFF IN REAL TIME
			txt = re.sub("(@(\w){1,15}(?!\w))","",txt)
			txt = re.sub("[^a-z0-9\s]","",txt)
			doc = nlp(txt)

			# Check if doc.ents is a list so you can do the next line correctly
			# print(f'This should be the text and then label: {}, {}')
			pdb.set_trace()
			# DON'T RUN ANYTHIG YET FINISH OPERATIONS IN HERE


	# txt=line['text']
	# tt=txt.lower()
	# ttt=re.sub("(@(\w){1,15}(?!\w))","",tt)
	# tttt=re.sub("[^a-z0-9\s]","",ttt)
	# doc=nlp(tttt)
	# [(X.text,X.label_) for X in doc.ents]

	# DELETE IF USING SPACY
	# # TODO 2: Set up a Named Entity Recognition module to perform a real time count of entities
	# st = StanfordNERTagger(
	#   CLASSIFIER,
	#   JAR_FILE,
	#   encoding='utf-8')

	# # INSPECT st.tag -> <Signature (self, tokens)>

	pdb.set_trace()


"""

# TRY USING SPACY