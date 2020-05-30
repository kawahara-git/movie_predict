import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

class Scraping:
    def get_class_info(self,soup,class_name):
        info=soup.find_all(class_=class_name)
        return info
    def generate_bs_object(self,movie_url,page=1):
        info=requests.get(movie_url,params={"page":page})
        status_code=info.status_code
        if status_code != 200:
            contents=None
        else:
            contents=BeautifulSoup(info.content,'lxml')
            time.sleep(1)
        return contents
    def get_avg_score(self,url):
        soup=Scraping.generate_bs_object(self,url)
        score_info=Scraping.get_class_info(self,soup,'c-rating__score')
        avg_score=score_info[0].text    
        return avg_score