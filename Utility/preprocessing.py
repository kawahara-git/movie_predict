import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

Scraping = Scraping()

class Preprocessing:
    def get_avg__data(self,BASE_URL,USER_INFO):
        #1.ユーザーURLの取得###################################
        user_url=BASE_URL + 'users/' + USER_INFO 
        #2.ユーザーURLにアクセス###################################
        #ユーザーの情報取得
        user_soup=Scraping.generate_bs_object(user_url)
        if user_soup==None:
            print('アクセスエラー')
        else:
            #タイトルとユーザースコアと平均スコア取得
            titles=Scraping.get_class_info(user_soup,'c-content-card__title')
            user_scores=Scraping.get_class_info(user_soup,'c-rating__score')
            urls=Scraping.get_class_info(user_soup,'c-content__jacket')
            #データフレーム作成
            columns=['Title','user_Score','avg_Score']
            data=pd.DataFrame(columns=columns)
            title_num = len(titles)
            for i in range(title_num):
                #タイトル取得
                title_all=titles[i].a.text
                title_year=titles[i].span.text
                title=title_all.replace(title_year,'').strip()
                #ユーザースコア取得
                user_score=user_scores[i].text
                #映画URLの生成
                movie_url=urls[i].get('href')
                movie_url = BASE_URL + movie_url
                #平均スコア取得
                avg_score=Scraping.get_avg_score(movie_url)
                csv = pd.Series([title,user_score,avg_score],columns)
                data=data.append(csv,columns)
                print("進行状況："+str(i+1)+"/"+str(title_num))
            data=data.set_index('Title')
            
            #data= pd.concat([user_data,data],axis=0)
            
            data.to_csv('test.csv',encoding='utf_8_sig')
        return None
