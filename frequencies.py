import csv
from utils import *

# # read the lexicons
lexTerms={}
with open('lexiconTerms.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        lexTerms[row[0]]=[]
        for i in range(1,len(row)):
            lexTerms[row[0]].append(row[i])

ps = PorterStemmer()
df = pd.DataFrame()
dictLength={}

def calculateFrequencies(myDictStem):
    print(myDictStem.keys())
    for k,v in myDictStem.items():
        print(len(v))
        for key,values in lexTerms.items():
            count=0
            for w in values:
                count = count + v.count(ps.stem(w))
            print(k, key, count)


  # #if __name__ == '__main__':
  # #    pathToTheFiles="/Users/anastasia/PycharmProjects/textAnalytics/AI-Policies-txt/"
  # #    readFiles(pathToTheFiles)
  # #
  # #    df['country'] = myDict.keys()
  # #    df['text'] = myDictOriginal.values()
  # #    df['tokens'] = myDict.values()
  # #    df['length'] = df['text'].astype(str).apply(len)
  # #    df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
  # #    #extract the named entities
  # #    preprocessedText=[]
  # #        # #Create your bigrams
        # bgs = nltk.bigrams(v)
        # #
        # # #compute frequency distribution for all the bigrams in the text
        # fdist = nltk.FreqDist(bgs)
        # print (fdist[(ps.stem('private'), ps.stem('information'))])
        #
        # #
        # #
        # #








