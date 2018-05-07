import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
from nltk.corpus import stopwords
from sqlalchemy.engine import create_engine
import json
import re
import nltk
#nltk.download('stopwords')

def save_object (table, row):

    keys = row.keys();
    sql = "INSERT INTO " + table + " ("
    sql = sql + ", ".join(keys)
    sql = sql + ") VALUES ("
    sql = sql + ", ".join([ ("'" + str(row[key]) + "'") for key in keys])
    sql = sql + ")"

    id = connection.execute(sql);

    return id

def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        for word in line.split( ): #in case more than one per line
            stopWords.append(word)
    return stopWords

def loadAffectiveDictionary(affectiveWordFile):
    affectiveWords = {}
    linecount = 0
    for line in open(affectiveWordFile):
        if linecount>2:
            words = line.split("\t")
            if words[0] not in affectiveWords:
                affectiveWords[words[0]] = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0,
                'positive': 0, 'sadness': 0, 'surprise': 0, 'trust':0 }
            affective_senses = affectiveWords[words[0]]
            affective_senses[words[1]] = int(words[2])
        linecount = linecount + 1
    return affectiveWords

# calculate affective senses counts
def affective_sense_counts(texts, affectivelexicon_dict):
	affective_senses_counts = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'negative': 0,
    'positive': 0, 'sadness': 0, 'surprise': 0, 'trust':0 }
	#affective_senses = 0
	for text in texts:
		for token in text:
			if token in affectivelexicon_dict:
				affective_senses = affectivelexicon_dict[token]
				for sense in affective_senses_counts:
				#affective_senses += affective_senses(sense)
					affective_senses_counts[sense] = affective_senses_counts[sense] + int(affective_senses[sense])

	affective_counts_json =  json.dumps(affective_senses_counts)
	return affective_counts_json

def processTweet2(tweet):
    # process the tweets
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    tweet = re.sub(r'\\([^\s]+)', ' ', tweet)
    #trim
    tweet = tweet.strip('\\')
    tweet = tweet.strip('\'"')
    return tweet

# remove common words and tokenize
def remove_stopwords(documents):
    stoplist = loadStopWords('stopwords.txt')
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    return texts

#load affective text lexicon
affectivelexicon_dict = loadAffectiveDictionary('NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt')

# Create database connection
documents = []
engine = create_engine("sqlite:///db.sqlite3")
connection = engine.connect()
#connection.close()

# Delete stored topics and affective lexicon counts
connection.execute("DELETE FROM fyp_project_mlcache");

# load documents (i.e. posts or messages containing cyberbullying traces) from database
sql = "SELECT message FROM fyp_project_Tweets"
result = connection.execute(sql);
for row in result:
    documents.append(row[0].replace('#039;',''))

theFile = open('tweets.txt', 'w')
for document in documents:
    theFile.write("%s\n" % document)

cyberbullyingdocs = remove_stopwords(documents)

affective_counts_cyberbullying_json = affective_sense_counts(cyberbullyingdocs, affectivelexicon_dict)

record = {'affective_counts_cyberbullying_json': affective_counts_cyberbullying_json.replace("'", "''")}
save_object ("fyp_project_mlcache", record)
connection.close()
