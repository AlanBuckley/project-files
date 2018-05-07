
from __future__ import division
import string
import re
from collections import Counter
import numpy
import matplotlib.pyplot as plt
from sqlalchemy.engine import create_engine
import os

### Constants: ###
lambda_value = 0.1
prior_class_probability_good = 0.6
prior_class_probability_bad = 0.4
alpha = 100
beta = 5
iters = 1000
max_epochs = 100

'''
String -> ListofWords
GIVEN: A filename
RETURNS: The list of words from that file, removing the punctions
         and in lower case
'''
def analyzer(filename):
    tokens=[]
    i=0
    review=open(filename,'r')
    with open(filename, encoding="utf8", errors='ignore') as f:
        for line in f:
            if i < 10000:
                words = [x.strip(string.punctuation) for x in line.lower().split()]
                tokens=tokens+words
                i=i+1
            else:
                break
    return tokens

'''
ListOfWords ListofWords -> Integer
GIVEN: Two list of words
RETURNS: The Counter and total vocabulary count from the two list of words
'''
def get_vocab_size(bad_tokens,good_tokens,test_tokens):
    overall_vocab=bad_tokens+good_tokens+test_tokens
    count = {}
    count = Counter(overall_vocab)
    return count,len(count)

'''
GIVEN: No arguments
RETURNS: The dictionary of test tweets
'''
def get_test_data():
    with open("tweets.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    import string
    dictionary_of_test_data={}
    i=0
    for line in content:

        words=[x.strip(string.punctuation) for x in line.lower().split()]
        dictionary_of_test_data["Tweet"+str(i)]=words
        i=i+1
    return dictionary_of_test_data

'''
Dictionary -> Dictionary
GIVEN: The test dictionary
RETURNS: Performs Naive_Bayes to the test data and returns the classification
         of test data as belonging to Abusive or Non Abusive Tweets in
         a dictionary of probabilities corresponding to that tweet
         good - corresponds to non abusive tweets
         bad - corresponds to abusive tweets
FORMULA: P(C|X) = P(X|C) * P(C) / P(X)
'''
def naive_bayes(dictionary_of_test_data):
    classification={}
    for test in dictionary_of_test_data.keys():
        tweet=dictionary_of_test_data[test]
        good_prob = get_probability(tweet,0)
        bad_prob= get_probability(tweet,1)
        classification[test]=[good_prob,bad_prob]
    return classification

'''
Dictionary -> File
GIVEN: The dictionary containing probability values
       of tweets after Naive Bayes and the threshold for classification
RETURNS: The results of tweets (as good or bad) onto
         Naive_Bayes_Model_Results.txt and the same as
         a dictionary
'''
def get_NB_results(NB_Classification, threshold):
    f = open("Naive_Bayes_Model_Results.txt",'w')
    answer_dict={}
    for key in NB_classification.keys():
        value = NB_classification[key]
        ratio = value[0]/value[1]
        if ratio < threshold:
            answer_dict[key]="Good"
            f.write(key+" "+"Good"+"\n")
        else:
            answer_dict[key]="Bad"
            f.write(key+" "+"Bad"+"\n")
    f.close()
    return answer_dict

'''
Dictionary ListofWords -> Float Float Float Float
GIVEN: The model output and expected output
RETURNS: The number of true positives, true negatives,
         false positives, false negatives
'''
def get_PR(NB_results,expected_output):
    tp=1
    tn=1
    fp=1
    fn=1
    for key in NB_results.keys():
        model_outcome = NB_results[key]
        expected_output_index = int(key.split('et')[1])
        expected_outcome = expected_output[expected_output_index]
        if model_outcome == 'Bad' and expected_outcome == 'Bad':
            tp = tp + 1
        elif model_outcome == 'Good' and expected_outcome == 'Bad':
            fn = fn + 1
        elif model_outcome == 'Bad' and expected_outcome == 'Good':
            fp = fp + 1
        else:
            tn = tn + 1
    return tp,tn,fp,fn

'''
GIVEN: No arguments
RESULTS: reads the expected output from Test_Answers.txt
         with line number corresponding to tweet number
         and the string corresponding to its classified
         class
'''
def read_actual_answers():
    f=open("Test_Answers.txt",'r')
    lines = f.readlines()
    answers=[]
    for i in range(len(lines)):
        answers=answers+[lines[i].split('\n')[0]]
    return answers

'''
ListofWords Integer -> Float
GIVEN: A tweet as a list of words and a number to denote the probability
       class (abusive or not) that we are trying to calculate
       num = 0 means non abusive tweets
       num = 1 means abusive tweets
RETURNS: The probability of tweet as belonging to that particular class
'''
def get_probability(tweet,num):
    prob=1
    if num==0:
        for word in tweet:
            if word in prob_good_words.keys():
                term1=prob_good_words[word]
                term2=prior_class_probability_good
                term3=vocab_counter[word]/vocab_size
                prob = prob * (term1 * term2) / term3
            else:
                term1=1/len(prob_good_words)
                term2=prior_class_probability_good
                term3=vocab_counter[word]/vocab_size
                prob = prob * (term1 * term2) / term3
        return prob
    else:
        for word in tweet:
            if word in prob_bad_words.keys():
                term1=prob_bad_words[word]
                term2=prior_class_probability_bad
                term3=vocab_counter[word]/vocab_size
                prob = prob * (term1 * term2) / term3
            else:
                term1=1/len(prob_bad_words)
                term2=prior_class_probability_bad
                term3=vocab_counter[word]/vocab_size
                prob = prob * (term1 * term2) / term3
        return prob

'''
Dictionary Integer -> Dictionary
GIVEN: a dictionary with (words & their counts) in a particular class
       and total number of words in that particular class
RETURNS: A probabilistic dictionary of those words
'''
def get_prob_dict(tokens_count, length):
    count={}
    for key in tokens_count.keys():
        count[key]=(tokens_count[key]+lambda_value)/(length + lambda_value * vocab_size)
    return count


def save_summaryobject (table, row):

    keys = row.keys();
    sql = "INSERT INTO " + table + " ("
    sql = sql + ", ".join(keys)
    sql = sql + ") VALUES ("
    sql = sql + ", ".join([ ("'" + str(row[key]) + "'") for key in keys])
    sql = sql + ")"

    id = connection.execute(sql);

    return id


### main() portion of the program ###
print ("starting main")
##
##Analyse the bad_corpus.txt, getting all the word counts
##and write them on to bad_counts.txt
##
bad_tokens=analyzer('bad_corpus.txt')
total_bad_words = len(bad_tokens)
bad_tokens_count = Counter(bad_tokens)
with open('bad_counts.txt','w')as g:
    for key in bad_tokens_count.keys():
        g.write(key+" "+str(bad_tokens_count[key]))
        g.write("\n")

##
##Analyse the good_corpus.txt, getting all the word counts
##and write them on to good_counts.txt
##
good_tokens=analyzer('good_corpus.txt')
total_good_words = len(good_tokens)
good_tokens_count = Counter(good_tokens)
with open('good_counts.txt','w', encoding="utf8", errors='ignore')as g:
    for key in good_tokens_count.keys():
        g.write(key+" "+str(good_tokens_count[key]))
        g.write("\n")

## get test data in the form of a dictionary of tweets ##
dictionary_of_test_data=get_test_data()

##
##Analyse the test_data.txt, getting all the word counts
##and write them on to test_counts.txt
##
test_tokens=analyzer("tweets.txt")
total_test_words = len(test_tokens)
test_tokens_count = Counter(test_tokens)
with open('test_counts.txt','w')as g:
    for key in test_tokens_count.keys():
        g.write(key+" "+str(test_tokens_count[key]))
        g.write("\n")

## get the total vocabulary size here ##
vocab_counter,vocab_size = get_vocab_size(bad_tokens,good_tokens,test_tokens)

## Get the probability counts ##
prob_bad_words=get_prob_dict(bad_tokens_count,total_bad_words)
prob_good_words=get_prob_dict(good_tokens_count,total_good_words)

## Write bad_prob_counts onto bad_counts_prob.txt ##
with open('bad_counts_prob.txt','w')as g:
    for key in prob_bad_words.keys():
        g.write(key+" "+str(prob_bad_words[key]))
        g.write("\n")

## Write good_prob_counts onto good_counts_prob.txt ##
with open('good_counts_prob.txt','w',encoding="utf8", errors='ignore')as g:
    for key in prob_good_words.keys():
        g.write(key+" "+str(prob_good_words[key]))
        g.write("\n")

## get test data in the form of a dictionary of tweets ##
dictionary_of_test_data=get_test_data()

## apply naive bayes here ##
print ("Naive Bayes Classifier")
NB_classification = naive_bayes(dictionary_of_test_data)

pr_dict={}
threshold=0
while threshold<max_epochs:
    # print "...writing NB results onto a file..."
    NB_results=get_NB_results(NB_classification,threshold)

    # print "...reading actual test results..."
    expected_output_list=read_actual_answers()

    ## PRECISION - RECALL values for naive bayes ##
    true_positives,true_negatives,false_positives,false_negatives = get_PR(NB_results,expected_output_list)
    if true_positives == 0:
        precision=0
        recall=0
    else:
        precision = true_positives/(true_positives + false_positives)
        recall = true_positives/(true_positives + false_negatives)
        pr_dict[str(threshold)]=[precision,recall]
        threshold = threshold + 0.01
print (" finished ")
print ("false_pos", false_positives)
print ("false_neg", false_negatives)
print ("true_pos", true_positives)
print ("true_neg", true_negatives)
y = true_positives/(true_positives + false_positives)
x = true_positives/(true_positives + false_negatives)
recall = round(x, 3)
precision = round (y, 3)

totalTweets = true_negatives + true_positives + false_negatives + false_positives

z = (2*recall*precision)/(recall+precision)
fScore = round(z, 1)
fScore = fScore*100
recall = recall*100
precision = precision*100
print ("f score", fScore)
print ("recall", recall)
print ("precision: ", precision)
engine = create_engine("sqlite:///db.sqlite3")
connection = engine.connect()

connection.execute("DELETE FROM fyp_project_cleanmessage");

record = {'recall': recall, 'precision': precision, 'true_positives':true_positives, 'false_positives':false_positives,
 'true_negatives':true_negatives, 'false_negatives':false_negatives, 'totalTweets':totalTweets, 'fScore':fScore}
save_summaryobject ("fyp_project_cleanmessage", record)
connection.close()
