import re, time
import nltk
import string
from collections import Counter
from nltk.corpus import stopwords
import win32com.client as wincl
import logging 
from nltk.probability import FreqDist
from datetime import datetime 

brown = nltk.corpus.brown
stoplist = stopwords.words('english')


import logging
formatter = logging.Formatter('%(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
logger = setup_logger('wrong_words', 'golden_words.log')

# second file logger
super_logger = setup_logger('all_words', 'word.log')


words = brown.words()
no_capitals = [word.lower() for word in words]
filtered = [word for word in no_capitals if word not in stoplist]
fdist = FreqDist(filtered)
print('lenght of the fdist ' + str(len(fdist)))
top_ten = fdist.most_common(40000)

speak = wincl.Dispatch("SAPI.SpVoice")

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

def catch_up():
    try:
        for line in reversed(list(open("word.log"))):
            print('were are here ')
            print(line)
            return int(line.split()[-1])
    except:
        return 0 
past = [x.split()[2] for x in  list(open('word.log'))]
count = catch_up() if catch_up else 0
print('count', count)
for x in top_ten[count:]:

    if len(x[0]) < 3:
        continue
    # duplicate words 
    if x[0] in past:
        continue
    else: 
        past.append(x[0])

    speak.Speak(x[0])
    start = datetime.now()
    sample = input('')
    sample_time = datetime.now() - start
    judgement = sample == x[0]
    print(judgement)
    if not judgement:
        logger.info(f'{x[0]} - {sample}')

    super_logger.info(f'{judgement} - {x[0]} - {sample} - {sample_time} - {start} brown coprus at {count}')
    count = count + 1 
