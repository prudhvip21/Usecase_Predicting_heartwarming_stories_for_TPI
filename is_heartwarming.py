#!/usr/bin/env python
# coding: utf-8

# In[10]:


from ExtractArticles import *
from Clean_FeatureExtract import *
import pandas as pd
import joblib
import sys

# In[18]:


def Content_and_Heading(article_link):
    '''Extract the content and heading from the article in given link if the article belongs to our subset of 
    processable sites
    currently processable sites are TimesofIndia, IndianExpress, TheBetterIndia'''
    article_df = pd.DataFrame(columns=['content','actual_heading'],index=[0])
    if 'timesofindia' in article_link:
        article_df.loc[0] = get_toi_data(article_link)
        article_df['clean_content'] = article_df['content'].apply(clean_toi)
    elif 'indianexpress' in article_link:
        article_df.loc[0] = get_ie_data(article_link)
        article_df['clean_content'] = article_df['content'].apply(clean_ie_data)
    elif 'thebetterindia' in article_link:
        article_df.loc[0] = get_tbi_data(article_link)
        article_df['clean_content'] = article_df['content'].apply(clean_articles)
    else:
        return "Currently can't process this article site, see the list of sites in __doc__ of the Content_and_Heading"
        
    return get_article_df_all_columns(article_df)


# In[30]:


def get_article_df_all_columns(article_df):
    '''Applies all necessary functions to extract necessary features for modeling'''
    article_df[['upper_count', 'upper_words', 'word_count', 'mean(each_word_len)', 'text_length', 'punct_count', 'numeric_count', 'unique_word_count']] = article_df.apply(get_basic_features,axis=1,result_type='expand')
    article_df['stop_words_percent'] = article_df['content'].apply(lambda val: stop_words_percent(val))


    article_df['content_sentiment'] = article_df['clean_content'].apply(get_document_sentiment)
    article_df['clean_content'] = rem_contractions(article_df['clean_content'][0])
    article_df['lemmatized_content'] = article_df['clean_content'].apply(lemmatize_with_postag)
    article_df['pos_content'] = article_df['lemmatized_content'].apply(pos_sentence)
    article_df[['most_used_adjectives','adj_count']] = article_df.apply(most_used_adjectives,axis=1,result_type='expand')
    article_df[['positive_score','negative_score']] = article_df.apply(pos_neg_score,axis=1,result_type='expand')
    article_df[['mean_adj_length','all_adjs']] = article_df.apply(mean_adjective_length,axis=1,result_type='expand')
    article_df['mean_adj_length'].fillna(0,inplace=True)
    article_df = norm_numerical_features(article_df)

    article_df['heading_sentiment'] = article_df['actual_heading'].apply(get_document_sentiment)
    article_df['lemmatized_heading'] = article_df['actual_heading'].apply(lemmatize_with_postag)
    article_df['pos_heading'] = article_df['lemmatized_heading'].apply(pos_sentence)

    count_vec = CountVectorizer(ngram_range=(2,3),max_features=300)


    doc_vector = pd.DataFrame()
    doc_vector = doc_vector.append(article_df['lemmatized_content'].apply(create_mean_w2v))
    doc_vector[['text_length','mean_adj_length','unique_word_count','norm_adj_count']] = article_df[['text_length','mean_adj_length','unique_word_count','norm_adj_count']].copy(deep=True)

    try:
        doc_vector['cd_jj_usage'] = get_pos_count_vec(count_vec,article_df['pos_content']).to_numpy()
    except KeyError:
        doc_vector['cd_jj_usage'] = 0

    doc_vector[['text_length','mean_adj_length','unique_word_count','adj_counmean_adjective_length','cd_jj_usage']] = doc_vector[['text_length','mean_adj_length','unique_word_count','norm_adj_count','cd_jj_usage']].apply(minmax_scale)

    return doc_vector, article_df


# In[22]:


def predict_article_class(article_link):
    import os
    doc_vector,article_df = Content_and_Heading(article_link)
    cur_dir = os.getcwd()
    print(cur_dir)
    trained_gnb = joblib.load(open(cur_dir+'/gnb.gz','rb'))
    pred = trained_gnb.predict(doc_vector.to_numpy())
    if pred == 0:
        print("Not Heartwarming")
    elif pred == 1:
        print("Heartwarming")
    else:
        print("Something went wrong, please try again")
    
    user_opinion = input('\nDid you feel the article heartwarming?(0-no/1-yes)')
    
    try:
        machine_predictions = pd.read_csv(cur_dir+'/machine_predictions.csv')
        if article_link in machine_predictions['link']:
            pass
        else:
            article_df['link'] = article_link
            article_df['machine_prediction'] = pred
            article_df['user_opinion'] = user_opinion
            machine_predictions = pd.concat([machine_predictions,article_df],axis=0)
            machine_predictions.to_csv(cur_dir+'/machine_predictions.csv',index=False)
    except FileNotFoundError:
        article_df['link'] = article_link
        article_df['machine_prediction'] = pred
        article_df['user_opinion'] = user_opinion
        article_df.to_csv(cur_dir+'/machine_predictions.csv',index=False)
     
