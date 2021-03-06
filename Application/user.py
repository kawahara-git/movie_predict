import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Utility.scraping import *
from Utility.valueowner import *

Scraping = Scraping()

BASE_URL = Valueowner.BASE_URL.value

class User:
    def get_user_data(self,USER_INFO):
        print("***** ユーザー情報取得開始 *****")
        #1.ユーザーURLの取得###################################
        user_url = BASE_URL + 'users/' + USER_INFO 
        #2.ユーザーURLにアクセス###################################
        #ユーザーの情報取得
        user_soup=Scraping.generate_bs_object(user_url)
        if user_soup==None:
            print("アクセスエラー")
        else:
            #タイトルとユーザースコア取得
            titles=Scraping.get_class_info(user_soup,'c-content-card__title')
            user_scores=Scraping.get_class_info(user_soup,'c-rating__score')
            urls=Scraping.get_class_info(user_soup,'c-content__jacket')
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
