import os
import numpy as np
from app.forms import RunToolForm
from scipy.special import softmax
from django.shortcuts import render
from torch.utils.data import DataLoader
from django.http import HttpResponseRedirect
from transformers import AutoTokenizer, AutoModel, AutoConfig, AutoModelForSequenceClassification
from social_scraper import PlatformFactory, SearchQuery, PlatformEnumeration

# Global Variables
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Model Settings
CUDA = False # set to true if using GPU (Runtime -> Change runtime Type -> GPU)
BATCH_SIZE = 32
MODEL = str(BASE_DIR) + "/twitter-xlm-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL, use_fast=True, local_files_only=True, model_max_length=512, use_auth_token=True)
config = AutoConfig.from_pretrained(MODEL, local_files_only=True, use_auth_token=True) # used for id to label name
model = AutoModelForSequenceClassification.from_pretrained(MODEL, local_files_only=True, use_auth_token=True)
if CUDA:
    model = model.to('cuda')
_ = model.eval()

# Index
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RunToolForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_disable = True
            
            # Build paths inside the project like this: BASE_DIR / 'subdir'.
            main_directory = os.path.join(BASE_DIR, 'tweets')
            
            # Download Tweets
            form_data = form.cleaned_data
            username = form_data['username']
            username_txt = main_directory + "/" + username + ".txt"
            
            tweets = download_tweets(main_directory, username)
            results = sentiment_analysis(username_txt)
            total_sentiments = sentiment_count(results)
            
            return render(request,'index.html', {'form_data': form.cleaned_data, 'form_disable': form_disable, 'main_directory': username, 'tweets': tweets, 'results': results, 'total_sentiments': total_sentiments})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunToolForm()

    return render(request, 'index.html', {'form': form})
    
def download_tweets(dir, username):
    os.chdir(dir)
    
    from tweety.bot import Twitter
    tweets = Twitter(str(username)).get_tweets(pages=10).to_dict()
    tweets = tweets['tweets'][0]['result']['tweets']
    tweets = [tweet for tweet in tweets if "https://t.co" not in tweet['tweet_body']]
    tweets = tweets[:-1]
    tweets = list(filter(None, tweets))
    
    with open(dir+"/"+str(username)+".txt", 'w', encoding = 'utf-8') as f:
        for tweet in tweets:
            f.write(tweet['tweet_body'] + '\n')
    
    return tweets
    
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
  
def forward(text, cuda=True):
  text = preprocess(text)
  encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
  if cuda:
    encoded_input.to('cuda')
    output = model(**encoded_input)
    scores = output[0].detach().cpu().numpy()
  else:
    output = model(**encoded_input)
    scores = output[0].detach().numpy()
  
  scores = softmax(scores, axis=-1)
  return scores
  
def sentiment_analysis(dataset_path):
    dataset = open(dataset_path, encoding = 'utf-8').read().split('\n')
    dataset = dataset[:-1]
    dataset = list(filter(None, dataset))
    dl = DataLoader(dataset, batch_size=BATCH_SIZE)
    all_preds = []
    for idx,batch in enumerate(dl):
        # print('Batch ', idx+1, ' of ', len(dl))
        text = preprocess(batch)
        scores = forward(text, cuda=CUDA)
        preds = np.argmax(scores, axis=-1)
        all_preds.extend(preds)
        
    results = []
    
    for index, tweet in enumerate(dataset):
      pred = all_preds[index]
      result = {'text': tweet, 'output': config.id2label[pred]}
      results.append(result)

    return results
    
def sentiment_count(tweets):
  from collections import Counter
  c = Counter()
  for item in tweets:
      c[item["output"]] += 1
  
  c = dict(c)
  return c