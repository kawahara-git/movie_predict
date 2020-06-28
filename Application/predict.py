import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Utility.scraping import *

Scraping = Scraping()

class Predict:
    #タイトル検索から検索結果を取得
    def predict_movie_score(self,train_x,train_y,test_x):
        print(train_x)
        print(train_y)
        print(test_x)
        
        predict_score = 4
        return predict_score
