#!/usr/bin/env python
# coding: utf-8

# ## Importing packages

# In[4]:


import os
import numpy as np
import pandas as pd
import re
from tqdm.notebook import tqdm
tqdm.pandas()

#Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer

#Feature engineering
from nltk import tokenize
from textblob import TextBlob
from nltk.corpus import stopwords
englishStopWords = stopwords.words('english')
from nltk import pos_tag
import gensim.models.keyedvectors as word2vec
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
from scipy.spatial.distance import cosine

#Transformations
from sklearn.preprocessing import minmax_scale


wv = word2vec.KeyedVectors.load_word2vec_format("/Users/gurumanikanta/Documents/DS-Analytics/GoogleNews-vectors-negative300.bin.gz",binary=True)


# In[6]:


def get_basic_features(df):
    '''Creates basic features for the given text'''
    text = str(df['content'])
    text_split = text.split()
    upper_count = 0
    upper_words = list()
    word_count = 0
    numeric_count = 0
    each_word_len = list()
    text_length = len(text)
    #sometimes punctuations might include space
    punct_count = len(re.sub('\w+','',text).split())
    unique_word_count = len(pd.value_counts(text_split).index)
    for word in text_split:
        word_count += 1
        each_word_len.append(len(word))
        if word.isupper() and len(word)>1:
            upper_count += 1
            upper_words.append(word)
        elif word.isnumeric():
            numeric_count += 1
    return upper_count, upper_words, word_count, np.mean(each_word_len), text_length, punct_count, numeric_count, unique_word_count


def stop_words_percent(text):
    '''find the percentage of stop words in each article'''
    try:
        words_in_text = text.split()
        return len([word for word in words_in_text if word in englishStopWords])/len(words_in_text)
    except:
        return 0


# ## The Better India preprocessing

# In[17]:


def clean_articles(text):
    '''cleans one article at a time - removes punctuation, leading and trailing unwanted text if any, standardize case
    and returns the tokenized text
    all the characters encoded are quotation marks, hifen or someother form of punctuation, either way we will be 
    removing them so its better to directly replace all the non-word charcters before decoding them to keep the number 
    of steps to a minimum'''

    try:
        temp = re.sub(".*(Also Read:.*$)",' ',text).lower().strip()
        temp = re.sub(r"\\x[a-z][0-9]*|\\x[0-9]*","'",temp)
        temp = re.sub(r"\W+|\\n",' ',temp)
        temp = re.sub(r"<(.*)?>",' ',temp)
        
        return temp
    except:
        return temp

    


# ## Indian Express preprocessing

# In[18]:


def clean_ie_data(text):
    try:
        content = re.sub('For all the latest India News, download Indian Express App',' ',text).strip().lower()
        content = re.sub(r"\\x[a-z][0-9]*|\\x[0-9]*","'",content)
        content = re.sub(r"\W+|\\n",' ',content)
        content = re.sub(r"<(.*)?>",' ',content)
        
        return content
    except:
        return content
    


# ## Times of India preprocessing

# In[19]:


def clean_toi(text):    
    '''cleans the text by removing new line, trailing and leading single quote, encoded characters. We do not have any html tags to clean'''
    try:
        temp = re.sub('Download The Times of India News App for Latest India News',' ',text).strip().lower()
        temp = re.sub(r"\\x[a-z][0-9]*|\\x[0-9]*","'",temp)
        temp = re.sub(r"\W+|\\n",' ',temp)
        temp = re.sub(r"<(.*)?>",' ',temp)
        
        return temp
    except:
        return temp


# ## Feature Extraction

# In[16]:


contractions = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

def rem_contractions(text):
    '''remove most used contractions based on the contractions dictionary'''
    text = str(text)
    rep = dict((re.escape(k), v) for k, v in contractions.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text


def lemmatize_with_postag(sentence):
    '''lemmatize the content with respect to the pos_tag'''
    sentence = str(sentence)
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags if wd not in englishStopWords]
    return " ".join(lemmatized_list)



def pos_sentence(text):
    '''converts a text with words to text with pos tags for the respective words'''
    text = str(text)
    words_and_tags = pos_tag(text.split())
    pos_sent = list()
    for word, tag in words_and_tags:
        pos_sent.append(tag)
        
    return ' '.join(pos_sent)



#from operator import itemgetter
def most_used_adjectives(row,top=5):
    '''returns the list of #top adjectives and the length of the list of all adjectives in a text'''
    text = str(row['lemmatized_content'])
    adj_list = list()
    #currently -3 index is lemmatized text
    sent_split = text.split()
    for word,tag in pos_tag(sent_split):
        if tag.lower() in ['jj','jjr','jjs']:
            adj_list.append(word)

    
    return list(pd.value_counts(adj_list).index[:top]),len(adj_list)


###most used adjectives similarity with words "good" and "bad" to determine the goodness of articles
def pos_neg_score(row):
    '''returns the average positive/negative scores based on top adjectives'''
    pos_score = 0
    neg_score = 0
    adjectives = row['most_used_adjectives']
    num_adj = len(adjectives)
    for adj in adjectives:
        try:
            pos_score = pos_score + wv.similarity(adj,'good')
        except:
            pass
        try:
            neg_score = neg_score + wv.similarity(adj,'neg')
        except:
            pass
    
    if num_adj == 0:
        avg_pos, avg_neg = 0, 0
    else:
        avg_pos, avg_neg = pos_score/num_adj, neg_score/num_adj
        
    return avg_pos, avg_neg




def doc_similarity_to_pos(sim_demo):
    '''calculates the similarity of all articles to the positive articles'''
    cos_sim = dict()
    vocab = wv.vocab
    for i in range(6628):
        pos_article = sim_demo['lemmatized_content'][i]
        if not pd.isnull(pos_article):
            pos_vec = np.mean([wv[word] for word in pos_article.split() if (word in vocab)],axis=0)
            cos_sim['article_'+str(i)] = list()
            for d in range(len(sim_demo)):
                demo_article = sim_demo['lemmatized_content'][d]
                if not pd.isnull(demo_article):
                    demo_vec = np.mean([wv[word] for word in demo_article.split() if (word in vocab)],axis=0)
                    cos_sim['article_'+str(i)].append(cosine(pos_vec,demo_vec))
                else:
                    cos_sim['article_'+str(i)].append(None)
        else:
            continue

    for key in cos_sim.keys():
        cos_sim[key] = np.mean(cos_sim['key'])

    sim_df = pd.DataFrame(data=cos_sim)
    return sim_df.apply(np.mean,axis=1)




####sentiments
def penn_to_wn(tag):
    '''Convert between the PennTreebank tags to simple Wordnet tags'''
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

lemmatizer = WordNetLemmatizer()
def get_document_sentiment(text):
    '''extracts sentiment of the given text'''
    text = str(text)
    score = 0.0
    tokens_count = 0
 
    tagged_text = pos_tag(tokenize.word_tokenize(str(text)))

    for word, tag in tagged_text:
        wn_tag = penn_to_wn(tag)
        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
            continue

        lemma = lemmatizer.lemmatize(word, pos=wn_tag)
        if not lemma:
            continue

        synsets = wn.synsets(lemma, pos=wn_tag)
        if not synsets:
            continue

        # The most commonly used form of the word
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())

        score += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1

    if not tokens_count:
        return 0
 
    return score/tokens_count


def mean_adjective_length(row):
    '''iterates one row at a time, identifies all adjectives and returns mean length of all adjectives'''
    text = str(row['lemmatized_content'])
    adj_list = list()
    adj_len_list = list()
    
    try:                
        sent_split = text.split()
        for word,tag in pos_tag(sent_split):
            if tag.lower() in ['jj','jjr','jjs']:
                adj_list.append(word)
                adj_len_list.append(len(word))
                

        return np.mean(np.array(adj_len_list)),' '.join(adj_list)
    except:
        return 0


def norm_numerical_features(all_data_temp):
    '''Creates a normalized feature for all the numerical features available'''
    all_data_temp['norm_adj_count'] = all_data_temp['adj_count']/all_data_temp['word_count']
    all_data_temp['norm_upper_count'] = all_data_temp['upper_count']/all_data_temp['word_count']
    all_data_temp['norm_numeric_count'] = all_data_temp['numeric_count']/all_data_temp['word_count']
    all_data_temp['norm_unique_word_count'] = all_data_temp['unique_word_count']/all_data_temp['word_count']
    all_data_temp['norm_punct_count'] = all_data_temp['punct_count']/all_data_temp['text_length']

    return all_data_temp


# ## word2vec word embeddings mean for article

# In[3]:


def create_mean_w2v(article):
    '''creates an average word embedding for the whole article by considering the collective mean of all word 
    embeddings of a given article''' 
    temp_df = pd.DataFrame()
    for word in set(article.split()):
        try:
            word_embed = wv[word]
            temp_df = temp_df.append(pd.Series(word_embed),ignore_index=True)
        except:
            pass
    return temp_df.mean()


# ## content_pos count vectorizer

# In[14]:


def get_pos_count_vec(count_vec,pos_content):
    '''Returns the tag combinations that have most impact on positivity of the articles, at this time it only returns
    "cd jj" '''
    pos_count_df = count_vec.fit_transform(pos_content)
    pos_count_df = pd.DataFrame(data = pos_count_df.toarray() , columns = count_vec.get_feature_names())
    
    return pos_count_df['cd jj']

