#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup as bs
from random import random,randint
from re import findall
from time import sleep


def get_tbi_data(link):
    '''extract heading and conent from the given tbi article link'''
    try:
        response = requests.get(link)
        sleep(random()*randint(1,8))
        soup = bs(response.content,'lxml')
        paras = soup.find_all('div',attrs={'class':'entry-content clr'})[0].find_all('p')
        heading = soup.find_all('h1')[0].get_text()
        
        return ' '.join([para.get_text() for para in paras]),heading
    except Exception as e:
        print('Error with: {}\nerror: {}'.format(link,e))
        return None
    

def get_ie_data(link):
    '''extract heading and content from the given indian express article link'''
    try:
        #get rid of multipage in for the content by adding a trailing 0
        response = requests.get(link+'/0/')
        sleep(random()*randint(1,8))
        soup = bs(response.content,'html.parser')
        content = ''
        for text in soup.find('span',attrs={'class':'custom-caption'}).find_all_next('p')[:-1]:
            content = content + ' ' + text.get_text()
        heading = soup.find('h1',attrs={'itemprop':'headline'}).text
        
        return content,heading
    except Exception as e:
        print("Error with: {}\nerror: {}".format(link,e))
        return None
    
    
def get_toi_data(link):
    '''extract heading and conent from the given Times of India articles'''
    cat_div_class = {'Normal' : ['entertainment','life-style','citizen-reporter','business','sports','tv','home',
                             'politics','gadgets-news','astrology','auto','most-searched-products','gaming',
                             'companies','nri','best-products','independence-day-2018','people','trend-tracking',
                            'spotlight','venture-capital','viral-news','web-series','times-fact-check',
                             'toi-homepage-slug','brandwire','global','toi-features'],
                 '_3WlLe clearfix' : ['city','india','elections','world']}
    try: 
        category = findall(".*?//.*?/(.*?)/.*",link)[0] 
    except Exception as e:
        print('Can not find article category from: {}\nerror: {}'.format(link,e))
        return None
    
    try:
        response = requests.get(link)
        sleep(random()*randint(1,8))
        soup = bs(response.content,'html.parser')
        heading = soup.find('h1').text
    except Exception as e:
        print('Error with: {}\nerror: {}'.format(link,e))
        return None
    
    if (category in cat_div_class['Normal']) and (response.status_code == 200):
        try:
            return soup.find_all('div',attrs={'class':'Normal'})[0].get_text(), heading
        except:
            return None
    elif (category in cat_div_class['_3WlLe clearfix']) and (response.status_code == 200):
        try:
            return soup.find_all('div',attrs={'class':'_3WlLe clearfix'})[0].get_text(), heading
        except:
            return None
    else:
        return None

