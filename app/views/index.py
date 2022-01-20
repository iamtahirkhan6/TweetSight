from django.shortcuts import render
from app.forms import RunToolForm

import os
import numpy as np
from scipy.special import softmax
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModel, AutoConfig

# Index
def index(request):
    context = {}
    context['form']= RunToolForm()
    return render(request, "index.html", context)
   
def download_tweets(username):
    query = SearchQuery(username)

    # Omit this when you want to get all tweets. This can take infinite time, so be careful
    query.setMaximumItemCount(3000)
    
    # This has no proper function other than providing feedback in console. can be omitted as well
    query.setVerboseEnabled(True)
    
    query.setStartDate(datetime.date(2015, 1, 15))
    query.setEndDate(datetime.date(2015, 1, 16))
    
    
    # Tweets will be saved to the "test.csv" file, open it with excel
    PlatformFactory.create(PlatformEnumeration.TWITTER).search(query).saveAsCSV("test.csv")
    return
    
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