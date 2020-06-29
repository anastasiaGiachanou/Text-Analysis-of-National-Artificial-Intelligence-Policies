from utils import *

if __name__ == '__main__':
    pathToTheFiles="AI-Policies-txt/"
    myDict,myDictStem=readFiles(pathToTheFiles)

    print(myDict.keys())
    print(myDictStem.keys())

    df['country'] = myDict.keys()
    df['text'] = myDictOriginal.values()
    df['tokens'] = myDict.values()

    #extract the named entities
    preprocessedText=[]

    for k,v in myDict.items():
        text=""
        text=" ".join(str(x) for x in v)
        preprocessedText.append(text)

    df['preprocessedText'] = preprocessedText

    # calculate the similarity bases on USE
    # USE.similarityWithUSE(df['preprocessedText'], df['country'])


