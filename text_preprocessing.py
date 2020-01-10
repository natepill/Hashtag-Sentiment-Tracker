import numpy as np
import pandas as pd
import keras

# Set nltk assets locally due to deployment issues with nltk corpora
import nltk
nltk.download('stopwords')
nltk.download('punkt')
# nltk.data.path.append('./nltk_data/')

import re, string, unicodedata
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

def clean_text(words):
    lemmatizer = WordNetLemmatizer()
    new_words = []
    for word in words:
        if word not in stopwords.words('english') and word != '':
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_word = re.sub(r'[^\w\s]', '', word)
            new_word = word.lower()
            lemma = lemmatizer.lemmatize(word, pos='v')
            new_words.append(lemma)

    return new_words


def normalize(words):
    return clean_text(words)
