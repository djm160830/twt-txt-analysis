Python version: Python 3.7.6  

Extracting Tweets in real time using python-twitter library and displaying the count of named entities returned by spaCy's named entity recognizer with matplotlib's pyplot. 

## How to run
#### Install requirements  
`$ pip install -r requirements.txt`
#### Set environment variable
`set PYTHONIOENCODING=utf-8` to avoid "<i>charmap codec can't encode character</i>" error.   
#### If you would like to redirect terminal output to text file
`$ set PYTHONIOENCODING=utf-8`  
`$ python hw5.py > results.txt`  
#### If you would like to view terminal output
`$	 python hw5.py`
#### If you would not like to view any terminal output
`$ python hw5.py > NUL`
## Expected results
Code will run for 20 seconds according to line 101 in hw5.py (`timeout = time.time()+20`). You may change it to make it run for longer.  
#### Terminal output (example)  
`<number>==RAW` refers to the raw Tweet.  
`====ENT` refers to the entities that were recognized in the Tweet.  
`==COUNT` refers to the total count for each entity so far.  
```
93==RAW: I miss Ed, Edd n Eddy. They made me believe that Jaw-breakers were something to die for and ill always cherish that
====ENT: [('Ed', 'PERSON'), ('Edd n Eddy', 'ORG'), ('Jaw-breakers', 'PERSON')]
==COUNT: {'ORG': 14, 'PERSON': 18, 'CARDINAL': 11, 'GPE': 8, 'TIME': 6, 'ORDINAL': 3, 'DATE': 9, 'LAW': 1, 'FAC': 8, 'WORK_OF_ART': 1, 'PERCENT': 1}


149==RAW: In case you missed it Trump lost Michigan for the 87th time, tonight.
====ENT: [('Trump', 'ORG'), ('Michigan', 'GPE'), ('87th', 'ORDINAL'), ('tonight', 'TIME')]
==COUNT: {'ORG': 23, 'PERSON': 40, 'CARDINAL': 18, 'GPE': 12, 'TIME': 8, 'ORDINAL': 6, 'DATE': 13, 'LAW': 1, 'FAC': 9, 'WORK_OF_ART': 2, 'PERCENT': 1, 'QUANTITY': 1, 'MONEY': 1, 'NORP': 2}


372==RAW: I knew sooner or later @Twitter will follow with stories and to be honest I’m not happy but whatever...I guess 🤦🏻‍♀️🤷🏻‍♀️
====ENT: [('Twitter', 'ORG')]
==COUNT: {'ORG': 59, 'PERSON': 124, 'CARDINAL': 31, 'GPE': 32, 'TIME': 12, 'ORDINAL': 10, 'DATE': 36, 'LAW': 1, 'FAC': 13, 'WORK_OF_ART': 4, 'PERCENT': 2, 'QUANTITY': 4, 'MONEY': 2, 'NORP': 11, 'LOC': 2, 'PRODUCT': 2}


409==RAW: What’s the move tonight Houston?
====ENT: [('tonight', 'TIME'), ('Houston', 'GPE')]
==COUNT: {'ORG': 66, 'PERSON': 127, 'CARDINAL': 33, 'GPE': 40, 'TIME': 16, 'ORDINAL': 10, 'DATE': 41, 'LAW': 1, 'FAC': 13, 'WORK_OF_ART': 5, 'PERCENT': 2, 'QUANTITY': 5, 'MONEY': 2, 'NORP': 11, 'LOC': 2, 'PRODUCT': 2}
```
#### matplotlib.pyplot bar graph
![matplotlib graph](https://github.com/djm160830/twt-txt-analysis/blob/master/bar_graph.png)

## Parameters used
###### locations  
Los Angeles, San Francisco, rural CA,  
Dallas, Houston, rural TX,  
rural & urbal NY,  
Boston, rural MA
###### languages
English
###### time intervals
Figure 1: 22:46:40.34 – 23:46:40.34 Tue 11/17/2020  
Figure 2: 08:15:09.65 – 9:15:09.65 Wed 11/18/2020  
Figure 3: 19:22:27.23 – 20:22:27.23 Wed 11/18/2020  
Figure 4: 22:44:49.51 – 23:44:49.51 Wed 11/18/2020  
Figure 5: 07:31:46.52 – 8:31:46.52 Thu 11/19/2020  
  
**NOTE**: Time interval is not an actual parameter used in python-twitter stream filter. I used a timeout created by `time.time() + <amount of time I want to collect tweets in seconds>` in line 101. 


