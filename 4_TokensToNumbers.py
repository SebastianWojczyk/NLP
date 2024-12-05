import string
import re
import pprint
def normalize(textNormalized):
    textNormalized = textNormalized.lower()

    #\s "white" chars
    textNormalized = re.sub(r"\s", ' ', textNormalized)
    textNormalized = re.sub(r"([.,:;!?-])", r" \1 ", textNormalized)
    textNormalized = re.sub(r" +", ' ', textNormalized)
    textNormalized = textNormalized.strip()

    return textNormalized;
    
def getVocabulary(text):
    rawVocabulary = []
    for w in text.split(" "):
        if w not in rawVocabulary:
            rawVocabulary.append(w)
    
    vocabularyDict = {}
    for word in rawVocabulary:
        wordOneHotVector = []
        for wordForOne in rawVocabulary:
            if word==wordForOne:
                wordOneHotVector.append(1)
            else:
                wordOneHotVector.append(0)
        vocabularyDict[word] = wordOneHotVector
    return vocabularyDict

def getWords(textNormalized):
    words = []
    for w in textNormalized.split(" "):
        words.append(w)
    return words

def getSentences(textNormalized, vocabulary):
    sentences = []
    for s in textNormalized.split("."):
        s = s.strip()
        if len(s) > 0:
            s += " ." #mozna dodac kropke gdyby ktos chcial
            
            words = getWords(s)
            
            sentenceOneHotVectors = []
            for word in words:
                sentenceOneHotVectors.append({"word": word, "oneHotVector": vocabulary[word]})
            
            sentenceBagOfWord = []
            for _ in vocabulary:
                sentenceBagOfWord.append(0)

            for word in sentenceOneHotVectors:
                for i in range(len(word["oneHotVector"])):
                    sentenceBagOfWord[i] += word["oneHotVector"][i]
            
            sentences.append({"sentence": s, "words": words, "oneHotVectors":sentenceOneHotVectors, "bagOfWords": sentenceBagOfWord})

    return sentences

def getSimilatiry(v1, v2):
    if len(v1) != len(v2):
        return 0
    else:
        s = 0
        for i in range(len(v1)):
            if v1[i]==v2[i]:
                s += 1
        return s / len(v1)
    
text = """a B C -A B .A b c; d:
B c A d e . a? b c D!"""
text = "Ala ma kota i Ola ma kota. Ala ma tez psa. Janek tez ma psa i rybki."
text = "a b c. a. a b. b a."

textNormalized = normalize(text)
vocabulary = getVocabulary(textNormalized)
sentences = getSentences(textNormalized, vocabulary)

#pprint.pprint(vocabulary)
#pprint.pprint(sentences)

for s in sentences:
    print("-"*20)
    print(s["sentence"])

    for w in s["oneHotVectors"]:
        print(w["oneHotVector"], w["word"])
    print("Bag of words:")
    print(s["bagOfWords"])
    print("Similarity:")
    for s_similar in sentences:
        similarity = getSimilatiry(s["bagOfWords"], s_similar["bagOfWords"])
        print(s_similar["bagOfWords"], similarity, '\t',s_similar["sentence"])
