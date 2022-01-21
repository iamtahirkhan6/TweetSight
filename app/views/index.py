from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.forms import RunToolForm

import os
import numpy as np
from scipy.special import softmax
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModel, AutoConfig
from social_scraper import PlatformFactory, SearchQuery, PlatformEnumeration
import datetime

# Index
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RunToolForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_disable = True
            from pathlib import Path

            # Build paths inside the project like this: BASE_DIR / 'subdir'.
            BASE_DIR = Path(__file__).resolve().parent.parent
            main_directory = os.path.join(BASE_DIR, 'tweets')
            
            # Download Tweets
            form_data = form.cleaned_data
            username = form_data['username']
            
            tweets = download_tweets(main_directory, username)
            
            return render(request,'index.html', {'form_data': form.cleaned_data, 'form_disable': form_disable, 'main_directory': username, 'tweets': tweets})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunToolForm()

    return render(request, 'index.html', {'form': form})
    
# def index(request):
#     context = {}
#     context['form']= RunToolForm()
#     return render(request, "index.html", context)
   
def download_tweets(dir, username):
    os.chdir(dir)

    from tweety.bot import Twitter
    tweets = Twitter("elonmusk").get_tweets(pages=1).to_dict()
    tweets = tweets['tweets'][0]['result']['tweets']
    tweets = [tweet for tweet in tweets if "https://t.co" not in tweet['tweet_body']]
    
    import pandas as pd
    tweet_series = pd.Series(tweet['tweet_body'] for tweet in tweets)
    
    with open(dir+"/"+str(username)+".txt", 'w', encoding = 'utf-8') as f:
        for tweet in tweets:
            f.write(tweet['tweet_body'] + '\n')
    
    return tweets
    
def csv_to_tex(csv_file):
    return
    
def preprocess(corpus):
  outcorpus = []
  for text in corpus:
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    new_text = " ".join(new_text)
    outcorpus.append(new_text)
  return outcorpus