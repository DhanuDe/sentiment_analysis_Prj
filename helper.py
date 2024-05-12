import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import string
import nltk
import pickle

from nltk.stem import PorterStemmer
ps = PorterStemmer()


with open('static/model/model.pickle', 'rb') as file:
    model = pickle.load(file)

with open('static/model/corpora/stopwords/english', 'r') as file:
    sw = file.read().splitlines()

vocab = pd.read_csv('static/model/vocab.txt',header = None)
tokens = vocab[0].tolist()

def remove_punctuatios(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def preprocessing(text):
    data = pd.DataFrame([text], columns =['tweet'])
    data['tweet'] = data['tweet'].apply(lambda x:" ".join(x.lower() for x in x.split()))
    data['tweet'] = data['tweet'].apply(lambda x:" ".join(re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags =re.MULTILINE) for x in x.split()))
    data['tweet'] = data['tweet'].apply(remove_punctuatios)
    data['tweet'] = data['tweet'].str.replace('\d+', '',regex = True)
    data['tweet'] = data['tweet'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
    data['tweet'] = data['tweet'].apply(lambda x: " ".join(ps.stem(x) for x in x.split()))
    return data['tweet']


def vectorizer(ds):
    vec_list = []
    
    for sent in ds:
        sent_list = np.zeros(len(tokens))
        
        for i in range(len(tokens)):
            if tokens[i] in sent.split():
                sent_list[i] = 1
        vec_list.append(sent_list)
    vec_list_new = np.asarray(vec_list,dtype = np.float32)
    return vec_list_new


def get_pred(vec_text):
    prediction = model.predict(vec_text)
    if prediction == 1:
        return 'negative'
    else:
        return 'positive'