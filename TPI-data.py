#!/usr/bin/env python
# coding: utf-8


############################################################################
#The Better India Articles - considered all positive
import os
#all the files at p_name are to be combined to one dataframe
p_name = '/Users/gurumanikanta/Documents/DS-Analytics/SupervisedLearning/TPI/scrapped_data'
all_files_tpi = os.listdir(path=p_name)


import pandas as pd
pd.set_option('display.max_columns',20)
raw_data_tpi = pd.DataFrame()
#concat all files together into a single dataframe
for file in all_files_tpi:
    raw_data_tpi = pd.concat([raw_data_tpi,pd.read_csv(p_name+'/'+file,encoding='unicode-escape')])


raw_data_tpi.head()


#Drop the Unnamed: 0, month columns and create an actual index 
raw_data_tpi.drop(labels=['Unnamed: 0','month'],axis=1,inplace=True)
raw_data_tpi.reset_index(drop=True,inplace=True)

#verify if all the raw_headings follow respective formats throughout
raw_data_tpi['headings_list_length'] = raw_data_tpi['heading'].apply(lambda val: len(eval(val)))

#they all follow a pattern throughout so we can delete headings_list_length
raw_data_tpi.drop(labels=['headings_list_length'],inplace=True,axis=1)
raw_data_tpi['actual_heading'] = raw_data_tpi['heading'].apply(lambda val: eval(val)[1])
raw_data_tpi.drop(labels=['heading'],axis=1,inplace=True)


from nltk.corpus import stopwords
englishStopWords = stopwords.words('english')

def stop_words_percent(text):
    '''find the percentage of stop words in each article'''
    words_in_text = text.split()
    return len([word for word in words_in_text if word in englishStopWords])/len(text.split())
    
raw_data_tpi['stop_words_percent'] = raw_data_tpi['content'].apply(lambda val: stop_words_percent(val))


#get the uppercase words and the count of upper case words in text
def get_basic_features(df):
    '''Creates basic features for the given text'''
    from re import findall
    from numpy import mean
    text = df['content']
    text_split = text.split()
    upper_count = 0
    upper_words = list()
    word_count = 0
    numeric_count = 0
    each_word_len = list()
    text_length = len(text)
    punct_count = len(findall(r"\W+",text))
    unique_word_count = len(pd.value_counts(text_split).index)
    for word in text_split:
        word_count += 1
        each_word_len.append(len(word))
        if word.isupper() and len(word)>1:
            upper_count += 1
            upper_words.append(word)
        elif word.isnumeric():
            numeric_count += 1
    return upper_count, upper_words, word_count, mean(each_word_len), text_length, punct_count, numeric_count, unique_word_count

raw_data_tpi[['upper_count', 'upper_words', 'word_count', 'mean(each_word_len)', 'text_length', 'punct_count', 'numeric_count', 'unique_word_count']] = raw_data_tpi.apply(get_basic_features, axis=1, result_type='expand')

def rem_contractions(text):
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
    from re import escape,compile
    # use these three lines to do the replacement
    rep = dict((escape(k), v) for k, v in contractions.items()) 
    pattern = compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[escape(m.group(0))], text)
        
    return text

raw_data_tpi['content'] = raw_data_tpi['content'].apply(rem_contractions)

def clean_articles(text):
    '''cleans one article at a time - removes punctuation, leading and trailing unwanted text if any, standardize case
     and returns the tokenized text'''
    from re import sub
    #eval(bytes(raw_data_tpi['content'][3].replace('\n',''),'utf8').decode('windows-1252'))
    """all the characters encoded are quotation marks, hifen or someother form of punctuation, either way we will be 
    removing them so its better to directly replace all the non-word charcters before decoding them to keep the number 
    of steps to a minimum"""
    
    ##########eval(b"There\x92s".decode('cp1252')) ---> keep this in mind, explore further steps
    
    demo = sub(r"\W+",' ',text.lower())
    #starts with anything followed by day space year then time(covered in .*) only once before finding space pm/am space once
    demo = sub(r"^.*?[0-9]{1,2}.*?[0-9]{4}.*?[0-9]{1,2}.*?[0-9]{1,2}.*?",' ',demo).strip()
    demo = sub(r"^(am)|(pm)",'',demo).strip()
    demo = sub(r"get the best positive stories straight into your inbox",'',demo)
    return demo

raw_data_tpi['clean_content'] = raw_data_tpi['content'].apply(clean_articles)
raw_data_tpi['is_positive'] = 1




#standardize dataframe to combine with the IE data
column_list = ['content','actual_heading','clean_content','upper_words','upper_count','word_count',
               'mean(each_word_len)','unique_word_count','punct_count','numeric_count','text_length',
               'stop_words_percent','is_positive']

raw_data_tpi = raw_data_tpi[column_list]


#################################################################################
#INDIAN EXPRESS - considered all negative
ie_path = '/Users/gurumanikanta/Documents/DS-Analytics/SupervisedLearning/TPI/IndianExpress/'
ie_files_list = os.listdir(ie_path)
ie_data = pd.DataFrame()
for file in ie_files_list:
    ie_data = pd.concat([ie_data,pd.read_csv(ie_path+file,encoding='unicode-escape')])
    

ie_data.rename(columns={'Heading':'actual_heading','Content':'content'},inplace=True)
ie_data.drop(labels=['Unnamed: 0'],inplace=True,axis=1)
ie_data.reset_index(drop=True,inplace=True)

from re import sub
ie_data['actual_heading'] = ie_data['actual_heading'].apply(lambda heading: sub(' - Indian Express $| - Indian Express$|\W+',' ',heading).strip())
ie_data['content'] = ie_data['content'].apply(lambda content: sub(r'\r\n|\r<p>','',content).strip())
ie_data['content'] = ie_data['content'].apply(rem_contractions)
ie_data['clean_content'] = ie_data['content'].apply(lambda content: sub(r"\W+",' ',content).lower())

ie_data[['upper_count', 'upper_words', 'word_count', 'mean(each_word_len)', 'text_length', 'punct_count', 'numeric_count', 'unique_word_count']] = ie_data.apply(get_basic_features,axis=1,result_type='expand')
ie_data['stop_words_percent'] = ie_data['content'].apply(lambda val: stop_words_percent(val))

ie_data['is_positive'] = 0
ie_data = ie_data[column_list]


#concat both the dataframes
all_data = pd.concat([raw_data_tpi,ie_data],ignore_index=True)
all_data.shape


from textblob import TextBlob
def lemmatize_with_postag(sentence):
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
    return " ".join(lemmatized_list)


all_data['lemmatized_content'] = all_data['clean_content'].apply(lemmatize_with_postag)


def pos_sentence(text):
    '''converts a text with words to text with pos tags for the respective words'''
    from nltk import pos_tag
    words_and_tags = pos_tag(text.split())
    pos_sent = list()
    for word, tag in words_and_tags:
        pos_sent.append(tag)
        
    return ' '.join(pos_sent)

all_data['pos_content'] = all_data['lemmatized_content'].apply(pos_sentence)

###############################################################################
#Exploratory Data Analysis and Viz

#word cloud representation of all target articles(positive ones)
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#word cloud with both positive and negative articles
wc = WordCloud(width=1200,height=900,background_color='white',min_font_size=10,stopwords=englishStopWords)
plt.axis('off')
plt.imshow(wc.generate(' '.join(raw_data_tpi['clean_content'].values)))
plt.imshow(wc.generate(' '.join(ie_data['clean_content'].values)))

dfs = [raw_data_tpi,ie_data]
pn = ['positive','negative']
#top 30 words before removing stopwords - positve and negative articles
for df,state in zip(dfs,pn):
    word_list = ' '.join(df['clean_content'].values).split()
    top_30_words = pd.value_counts(word_list)
    print('{}:\n{}'.format(state,top_30_words[:31]))

##not at all helpful, since most of those are common words for every day speech - the,a,that,an,with...


#top 30 words after removing stopwords
word_list_no_stop = [word for word in word_list if word not in englishStopWords]

#faster way to remove stopwords, almost twice as fast as cached process because dictionaries work faster
stop_words_dict = pd.value_counts(englishStopWords)

for df,state in zip(dfs,pn):
    word_list = ' '.join(df['clean_content'].values).split()
    temp_no_stop = [word for word in word_list if word not in stop_words_dict]
    top_30_words = pd.value_counts(temp_no_stop)
    print('{}:\n{}'.format(state,top_30_words[:31]))

#the articles centric to children, education, villages, community development and India are most positive
#negative articles are very random, very high usage of politial terms but that doesn't say anything for sure



#histogram for the count variables
cols = ['upper_count','word_count','unique_word_count','punct_count','numeric_count']
dist_cols = ['text_length','mean(each_word_len)','stop_words_percent']
fig,ax = plt.subplots(nrows=2,ncols=3,figsize=(12,8))
fig.suptitle('Histogram for all count variables')
fig.tight_layout(h_pad=2)
fig.subplots_adjust(top=0.9)
ax = ax.flatten()
for i,col in zip(range(len(cols)),cols):
    ax[i].hist(all_data[col],bins=30)
    ax[i].set_xlabel(col)

#distplots for other variables
import seaborn as sns
fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(9,3))
fig.suptitle('Distribution of positive vs negative articles')
fig.tight_layout(h_pad=2)
fig.subplots_adjust(top=0.9)
ax = ax.flatten()
for i,col in zip(range(len(dist_cols)),dist_cols):
    sns.distplot(all_data[all_data['is_positive']==1][col],ax=ax[i],rug=True,label='positive')
    sns.distplot(all_data[all_data['is_positive']==0][col],ax=ax[i],rug=True,label='negative')
    ax[i].set_xlabel(col)
    


#word count vs upper case word count
plt.scatter(raw_data_tpi['upper_count'],raw_data_tpi['word_count'])
plt.title('Uppercase words count relative to the total word count')
plt.xlabel('Uppercase words')
plt.ylabel('Total words')
#not very clear but evedently number of uppercase words increase with increase in total words
#however, articles with word length upto 1200 have the highest possibility of atleast few uppercases
all_data[['upper_count','word_count']].corr()
#there is a 0.4 correlation

raw_data_tpi['mean(each_word_len)'].plot(kind='kde')
plt.title('Distribution of mean length')
sns.distplot(raw_data_tpi['mean(each_word_len)'],kde=True,hist=True,rug=True)
plt.xlabel('mean length of words')
plt.ylabel('density')
#most words have a length of 5 characters


longer_than_10k = all_data[all_data['text_length']>10000].index
#there are 120 articles having more than 10k characters and afer a random check it seems they aren't bogus

#word_count is very positively corelated to  many features
#interestingly mean_word_len and numeric_count are negatively corelated to stop_words_percent
#corelation of the target to any variable is very small or even 0. Given the volume and distinguishability of data it makes sense
sns.heatmap(all_data.corr())

#How do the basic features affect positivity of an article?
sns.facetgrid() 




########################################################################################
#modeling
#convert the documents to tfidf matrix
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(ngram_range=(1,2),max_features=350)
tfidf_pos = TfidfVectorizer(ngram_range=(1,3),max_features=100)


#our data is imbalanced, so using stratified sampling makes sense
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
skf = StratifiedShuffleSplit(n_splits=1,random_state=3)
for train_ind, test_ind in skf.split(X = np.zeros(len(all_data)),y = np.array(all_data['is_positive'])):
    train_ind, test_ind = train_ind,test_ind
    
X_train, X_test = all_data['clean_content'][train_ind], all_data['clean_content'][test_ind]
pos_X_train, pos_X_test = all_data['pos_content'][train_ind], all_data['pos_content'][test_ind]
y_train, y_test = all_data['is_positive'][train_ind], all_data['is_positive'][test_ind]

tfidf_train_pos = tfidf_pos.fit_transform(pos_X_train).toarray()
tfidf_train_data = tfidf.fit_transform(X_train).toarray()
train_features = np.append(tfidf_train_data,tfidf_train_pos,axis=1)

tfidf_test_data = tfidf.fit_transform(X_test).toarray()
tfidf_test_pos = tfidf_pos.fit_transform(pos_X_test).toarray()
test_features = np.append(tfidf_test_data,tfidf_test_pos,axis=1)

train_label = y_train
test_label = y_test

#after stratifiedshufflesplit the ratio of pos and neg remains same as expected
pd.value_counts(train_label)


#most corelated uni and bi grams
from sklearn.feature_selection import chi2
for val in [0,1]:
    ind = np.argsort(chi2(train_features,train_label==val)[0])
    feature_names = np.array(tfidf.get_feature_names())[ind]
    uni = [fn for fn in feature_names if len(fn.split())==1] 
    bi = [fn for fn in feature_names if len(fn.split())==2]
    print('Most corelated uni and bi grams for {}'.format(val))
    print('UNI: {}'.format(uni))
    print('BI: {}'.format(bi))


#baseline model Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
log_reg = LogisticRegression().fit(train_features,train_label)
pred = log_reg.predict(test_features)
accuracy_score(pred,y_test) 
#this is the expected behavior of a baseline model, predicts all entries of majority class exactly
#the difference between both class is too less for the model to identify correctly

#majority class percent
label_per = pd.value_counts(all_data['is_positive'])
label_per[0]/(label_per[0]+label_per[1])


#lets look at some advanced models to see if they can do a better job given our data

from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import RandomizedSearchCV

#the default svm model and parameters
svm_mod = svm.SVC(random_state=3)
print(svm_mod.get_params())

###Lets define some Hyperparameters to tune
C = [.0001, .001, .01]
degree = [1, 2, 3, 4, 5]
kernel = ['linear', 'rbf', 'poly']
probability = [True]
gamma = ['scale']


random_grid = {'C': C,
              'kernel': kernel,
              'degree': degree,
              'probability': probability,
              'gamma':gamma
             }


rand = RandomizedSearchCV(estimator=svm_mod, param_distributions=random_grid, n_iter=10, scoring='accuracy', 
                          cv=3, verbose=1, random_state=3)

rand.fit(train_features,train_label)

print('best_parameters:svm {}'.format(rand.best_params_))
print('best_accuracy:svm {}'.format(rand.best_score_))    

best_svm = svm.SVC(probability= True, kernel= 'linear', degree= 5, C= 0.0001,random_state=3,gamma='scale')
best_svm.fit(train_features,train_label)
pred = best_svm.predict(test_features)
classification_report(y_true=test_label,y_pred=pred)
confusion_matrix(y_true=test_label,y_pred=pred)
accuracy_score(y_true=test_label,y_pred=pred)
#the model has 97% accuracy but is incapable of predicting positive articles

#####Decision Tree
from sklearn.tree import DecisionTreeClassifier

#default model
dtc_mod = DecisionTreeClassifier(random_state=3)
print(dtc_mod.get_params())
#default parameters
'''{'class_weight': None, 'criterion': 'gini', 'max_depth': None, 'max_features': None, 'max_leaf_nodes': None, 
'min_impurity_decrease': 0.0, 'min_impurity_split': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 
'min_weight_fraction_leaf': 0.0, 'presort': False, 'random_state': 3, 'splitter': 'best'}'''

#tuning few hyperparameters
random_grid = {'criterion':['gini','entropy'],
               'max_depth':[20,50,80]}

rand = RandomizedSearchCV(estimator = dtc_mod, param_distributions=random_grid, n_iter=10, scoring='accuracy', cv=3, 
                          verbose=1, random_state=3)

rand.fit(train_features,train_label)

print('best parameters:dtc {}'.format(rand.best_params_))
print('best accuracy:dtc {}'.format(rand.best_score_))

#best parameters:dtc {'max_depth': 20, 'criterion': 'gini'}
#best accuracy:dtc 0.9731305602308247

best_dtc = DecisionTreeClassifier(criterion='gini',max_depth=20)
best_dtc.fit(train_features,train_label)
pred = best_dtc.predict(test_features)

print(classification_report(y_true=test_label,y_pred=pred))
print(confusion_matrix(y_true=test_label,y_pred=pred))
print(accuracy_score(y_true=test_label,y_pred=pred))

#though the accuracy is lesser than svm, looks like dtc is able to differentiate pos and neg better than svm



#######KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier

knc_mod = KNeighborsClassifier()
print('default parameters: {}'.format(knc_mod.get_params()))


random_grid = {'weights':['uniform','distance'],
               'n_neighbors':[3,5,7,10,12], 
               'p':[1,2]}

rand = RandomizedSearchCV(estimator=knc_mod, param_distributions=random_grid, n_iter=10, scoring='accuracy', cv=3,
                          random_state=3)

rand.fit(train_features,train_label)
print('best parameters:knc {}'.format(rand.best_params_))
print('best accuracy:knc {}'.format(rand.best_score_))








