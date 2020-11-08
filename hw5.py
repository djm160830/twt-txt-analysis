# NAME:			Darla Maneja
# EMAIL:		djm160830@utdallas.edu
# SECTION:		CS4372.001
# Assignment 5

import twitter
import os
from dotenv import load_dotenv
import nltk

# DELETE IF USING SPACY
# from nltk.tag import StanfordNERTagger
# from nltk.tokenize import word_tokenize

# Debugging
import inspect
import pdb

# DELETE IF USING SPACY
# Set java.exe location
# os.environ['JAVAHOME'] = "C:\\Program Files\\Java\\jdk-13.0.1\\bin\\java.exe"

project_folder = os.getcwd()  # Get current directory
load_dotenv(os.path.join(project_folder, '.env')) # Read from .env

# Twitter API
API_KEY=os.getenv('API_KEY')
API_KEY_SECRET=os.getenv('API_KEY_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('ACCESS_TOKEN_SECRET')
# Stream filter parameters
USERS=['@twitter']
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

if __name__ == "__main__":
	# Set up a listener
	api = listener()

	# Get a filtered view of public statuses
	# NOTE: check if there is a line['extended_tweet']['full_text'] before line['text']
	for i, line in enumerate(api.GetStreamFilter(track=USERS, languages=LANGUAGES)):
		if i==0: break;

	# DELETE IF USING SPACY
	# # TODO 2: Set up a Named Entity Recognition module to perform a real time count of entities
	# st = StanfordNERTagger(
	# 	CLASSIFIER,
	# 	JAR_FILE,
	# 	encoding='utf-8')

	# # INSPECT st.tag -> <Signature (self, tokens)>

	pdb.set_trace()




# TRY USING SPACY