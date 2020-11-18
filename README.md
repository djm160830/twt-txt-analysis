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
`$ python hw5.py`
#### If you would not like to view any terminal output
`$ python hw5.py > NUL`
## Expected results

#### Terminal output (example)
```
1==RAW: Wind 0.0 mph -. Barometer 30.009 in, Falling quickly. Temperature 38.0 °F. Rain today 0.00in. Humidity 77%
==ENT: [('0.0 mph', 'QUANTITY'), ('30.009', 'CARDINAL'), ('38.0', 'CARDINAL'), ('0.00', 'CARDINAL'), ('77%', 'PERCENT')]


3==RAW: Chameleon #vibes
🦎 #mattpratt #actor #losangeles #hi #casting #la @ Los Angeles, California https://t.co/aZ6ekHSVLQ
==ENT: [('Chameleon', 'ORG'), ('Los Angeles', 'GPE'), ('California', 'GPE')]


4==RAW: @realDonaldTrump Moron
==ENT: [('Donald Trump Moron', 'PERSON')]


5==RAW: 23:51 Temp. 71.6°F, Hum. 75%, Dewp. 61.3°F, Bar. 29.91 inHg, Rain Today 0 inch, Wind 229° 2.1 kn
==ENT: [('23:51', 'CARDINAL'), ('71.6', 'CARDINAL'), ('Hum', 'PERSON'), ('75%', 'PERCENT'), ('Dewp', 'ORG'), ('61.3', 'CARDINAL'), ('29.91', 'CARDINAL'), ('Hg', 'GPE'), ('Rain Today 0', 'PERSON'), ('229', 'CARDINAL')]
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
1:10am to 2:10am  
9:40am to 10:00am*  
10:19am to 11:19am*  
1:00pm to 2:00pm  
3:00pm to 4:00pm

\* = Interval may have been shortened due to internet connection.  
**NOTE**: Time interval is not an actual parameter used in python-twitter stream filter. I used a timeout created by `time.time() + <amount of time I want to collect tweets in seconds>` in line 104. 


