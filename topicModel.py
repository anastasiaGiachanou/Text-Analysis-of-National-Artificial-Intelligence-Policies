from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os, re
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim import corpora, models

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# spacy for lemmatization
import spacy
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt


def showVIS(lda_modelVIS, numTopics):
    vis = pyLDAvis.gensim.prepare(lda_modelVIS, corpus, dictionary_LDA)
    ##pyLDAvis.show(vis)
    pyLDAvis.save_html(vis, 'lda'+str(numTopics)+'.html')

def compute_coherence_values(dictionary, corpus, texts, start, limit, step):

    coherence_values = []
    model_list = []

    for num_topics in range(start, limit, step):

        print('NUMBER OF TOPICS: ', num_topics)
        model = models.LdaModel(corpus, num_topics=num_topics,
                                  id2word=dictionary_LDA,
                                  passes=50, alpha='auto',
                                  eta=[0.01]*len(dictionary_LDA.keys()))
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

        # print the extracted topics
        for i,topic in model.show_topics(formatted=True, num_topics=num_topics, num_words=15):
            print(str(i)+": "+ topic)
            print()
        print(coherencemodel.get_coherence())
        N=len(model[corpus])

        # calculate the probability of a topic in a document by averaging the scores
        for i in range(0,N):
            country = ''.join(i for i in df['country'][i] if not i.isdigit())

            for a in model[corpus[i]]:
                if a[0] in overallScores[country].keys():
                    overallScores[country][a[0]] = overallScores[country][a[0]] + a[1]
                    topicsPerCountry[country][a[0]] = topicsPerCountry[country][a[0]] + 1
                else:
                    overallScores[country][a[0]] = 0
                    topicsPerCountry[country][a[0]] = 1
                    overallScores[country][a[0]] = overallScores[country][a[0]] + a[1]

        print (overallScores)
        print (topicsPerCountry)

        # average probability of a topic in a document
        for country,scores in overallScores.items():
            for t,s in scores.items():
                avg=float(s)/float(topicsPerCountry[country][t])
                print(country, ",", t, ",",avg)

        #show a visualisation on the topics
        #showVIS(model,num_topics)
    return model_list, coherence_values


def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN','ADJ','ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])

    return texts_out

def readFiles(pathToTheFiles):
    allFiles=listAllFiles(pathToTheFiles)
    for f in allFiles:

        if ('.DS' in f):
            continue

        pdfFileObject = open(pathToTheFiles+f, 'r')
        allTextOfPDF = pdfFileObject.read()
        myDictOriginal[f.replace('.txt','')] = allTextOfPDF
        overallScores[f.replace('.txt','')] = {}
        topicsPerCountry[f.replace('.txt','')] = {}

def listAllFiles(path):
    return os.listdir(path)

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

if __name__ == '__main__':
    ps = PorterStemmer()
    overallScores={}
    topicsPerCountry={}

    stop_words = stopwords.words('english')
    spacy_nlp = spacy.load('en_core_web_sm')
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    stop_words.extend(['japan', 'germany','lithuania', 'malta','portugal','norway','france','italy','estonia','czech','republic','norway','luxembourg','india',
                       'australia','austria','finland','sweden','france','spain','denmark','singapore','serbia','USA','america'])
    stop_words.extend(['japanese','german','spanish', 'austrian','swedish', 'french','italian','norwegian','australian','russian','finnish','estonian','indian','estonian',
                       'lithuanian','portuguese','maltese','american','danish','american'])
    stop_words.extend(['http','https','federal','artificial','intelligence'])
    stop_words.extend(spacy_stopwords)

    myDict={}
    myDictOriginal={}
    df = pd.DataFrame()

    pathToTheFiles="AI-Policies-txt/"
    readFiles(pathToTheFiles)
    myDictOriginalParagraphs={}

    #split into paragraphs
    for k,i in myDictOriginal.items():
        sentences=i.split('\n\n')
        for count in range(0,len(sentences)-1):
            myDictOriginalParagraphs[k + str(count)]=sentences[count]

    df['country'] = myDictOriginalParagraphs.keys()
    df['text'] = myDictOriginalParagraphs.values()

    # removing everything except alphabets`
    df['clean_doc'] = df['text'].str.replace("[^a-zA-Z#]", " ")

    # remove short words
    df['clean_doc'] = df['clean_doc'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

    # make all text lowercase
    df['clean_doc'] = df['clean_doc'].apply(lambda x: x.lower())

    # tokenization
    tokenized_doc = df['clean_doc'].apply(lambda x: x.split())

    # remove stop-words
    tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words])
    data_words = tokenized_doc

    # de-tokenization
    detokenized_doc = []
    for i in range(len(df)):
        t = ' '.join(tokenized_doc[i])
        detokenized_doc.append(ps.stem(t))

    df['clean_doc'] = detokenized_doc

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words,threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=1)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # trigrams
    data_words_bigrams = make_bigrams(data_words)
    nlp = spacy.load('en', disable=['parser', 'ner'])

    # keep only nouns, adjectives and adverbs
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN','ADJ','ADV'])

    dictionary_LDA = corpora.Dictionary(data_lemmatized)
    dictionary_LDA.filter_extremes()

    texts = data_lemmatized
    corpus = [dictionary_LDA.doc2bow(text) for text in texts]

    # run the topic model for various number of topics and calculate the coherence score
    model_list, coherence_values = compute_coherence_values(dictionary=dictionary_LDA, corpus=corpus, texts=data_lemmatized, start=2, limit=15, step=1)

    #
    # # Show graph with the coherence scores
    limit=15; start=2; step=1;
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig('coherenceScores.jpg')





