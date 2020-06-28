import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Utility.valueowner import *

BASE_URL = Valueowner.BASE_URL.value

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
    def get_avg_score(self,urls):
        print("***** 平均値取得開始 *****")
        columns=['AvgScore']
        data=pd.DataFrame(columns=columns)
        for i,url in enumerate(urls):
            # #映画URLの生成
            movie_url=url.get('href')
            movie_url = BASE_URL + movie_url
            soup=Scraping.generate_bs_object(self,movie_url)
            score_info=Scraping.get_class_info(self,soup,'c-rating__score')
            avg_score=score_info[0].text
            csv = pd.Series([avg_score],columns)
            data=data.append(csv,columns)
            print("進行状況："+str(i+1)+"/"+str(len(urls)))
        #data=data.set_index('AvgScore')
        data.to_csv('test3.csv',encoding='utf_8_sig')
        print("***** 平均値取得完了 *****")
        return data
    
    def get_user_data(self,USER_INFO):
        print("***** ユーザー情報取得開始 *****")
        #1.ユーザーURLの取得###################################
        user_url = BASE_URL + 'users/' + USER_INFO 
        #2.ユーザーURLにアクセス###################################
        #ユーザーの情報取得
        user_soup=Scraping.generate_bs_object(self,user_url)
        if user_soup==None:
            print("アクセスエラー")
        else:
            #タイトルとユーザースコア取得
            titles=Scraping.get_class_info(self,user_soup,'c-content-card__title')
            user_scores=Scraping.get_class_info(self,user_soup,'c-rating__score')
            urls=Scraping.get_class_info(self,user_soup,'c-content__jacket')
            #データフレーム作成
            columns=['Title','UserScore']
            data=pd.DataFrame(columns=columns)
            title_num = len(titles)
            print("ユーザーの作品登録数："+str(title_num))
            for i in range(title_num):
                #タイトル取得
                title_all=titles[i].a.text
                title_year=titles[i].span.text
                title=title_all.replace(title_year,'').strip()
                #ユーザースコア取得
                user_score=user_scores[i].text
                csv = pd.Series([title,user_score],columns)
                data=data.append(csv,columns)
            #data=data.set_index('Title')
            data.to_csv('test.csv',encoding='utf_8_sig')
            print("***** ユーザー情報取得完了 *****")
        return data, urls
