import os
import pandas as pd
import re
from nltk.corpus import stopwords
import spacy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import USE,frequencies


lem = WordNetLemmatizer()
ps = PorterStemmer()
import plots

spacy_nlp = spacy.load('en_core_web_sm')
stopwords = stopwords.words('english')
myDict={}
myDictOriginal={}
myDictStem={}
df = pd.DataFrame()

def listAllFiles(path):
    return os.listdir(path)

def preprocess(text):
    tokens = []
    review = text.lower() #Convert to lower-case words
    raw_word_tokens = re.findall(r'(?:\w\w+)', review,flags = re.UNICODE) #remove pontuaction
    word_tokens = [w for w in raw_word_tokens if not w in stopwords] # do not add stop words
    tokens.extend(word_tokens)
    return tokens

def preprocessWithStem(text):
    tokens = []
    review = text.lower() #Convert to lower-case words
    raw_word_tokens = re.findall(r'(?:\w\w+)', review,flags = re.UNICODE) #remove pontuaction
    word_tokens = [ps.stem(w) for w in raw_word_tokens if not w in stopwords] # do not add stop words
    tokens.extend(word_tokens)
    return tokens

def readFiles(pathToTheFiles):
    allFiles=listAllFiles(pathToTheFiles)
    for f in allFiles:

        if ('.DS' in f):
            continue
        pdfFileObject = open(pathToTheFiles+f, 'r')
        allTextOfPDF = pdfFileObject.read()
        myDict[f.replace('.txt','')] = preprocess(allTextOfPDF)
        myDictStem[f.replace('.txt','')] = preprocessWithStem(allTextOfPDF)
        myDictOriginal[f.replace('.txt','')] = allTextOfPDF

    return myDict,myDictStem

