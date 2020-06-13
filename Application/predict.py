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
    def get_movie_search_url(self,BASE_URL,movie_title):
        #検索結果URLの生成
        search_root_front='search/movies?'
        search_root_end='&view=rich'
        search_title='q='+movie_title
        search_url = BASE_URL +search_root_front+search_title+search_root_end
        return search_url
    def get_movie_url(self,BASE_URL,movie_title):
        movie_search_url=Movie.get_movie_search_url(self,BASE_URL,movie_title)
        movie_search_soup =Scraping.generate_bs_object(movie_search_url)
        #print(movie_search_soup)
        #検索結果からタイトルとURL情報取得
        titles = Scraping.get_class_info(movie_search_soup,'p-content-cassette__title')
        #print(titles)
        #urls=get_class_info(movie_search_soup,'p-movie-cassette__readmore')
        #映画URLの生成
        url_list=re.findall('"movie_id":[0-9]{3,5}',str(movie_search_soup))
        url_list=sorted(set(url_list), key=url_list.index)
        url_list=re.findall('[0-9]{3,5}',str(url_list))
        for i in range(len(titles)):
            if titles[i].text == movie_title:
                url = url_list[i]
                movie_url = BASE_URL + 'movies/' + url
                break
            elif (i == len(titles)-1) & (titles[i].text != movie_title):
                movie_url=None
            else :
                pass
        return movie_url
    #映画データ取得
    def get_movie_data(self,BASE_URL,movie_title):
        #映画の情報取得
        movie_url = Movie.get_movie_url(self,BASE_URL,movie_title)
        movie_soup = Scraping.generate_bs_object(movie_url)
        #映画視聴者情報取得
        movie_record_users=Scraping.get_class_info(movie_soup,'c-media')
        #映画視聴者URLと視聴者スコア取得
        movie_record_users_urls=re.findall('"/users/(.*?)"',str(movie_record_users))
        movie_record_users_scores=re.findall('<div class="c-rating__score">(\d+\.\d|-)',str(movie_record_users))
        #データフレーム作成
        columns=['URL','movie_Score']
        data=pd.DataFrame(columns=columns)    
        for i in range(len(movie_record_users)):
            #URL取得
            movie_record_users_url=movie_record_users_urls[i]
            movie_record_users_url = BASE_URL + movie_record_users_url
            #スコア取得
            movie_record_users_score=movie_record_users_scores[i]
            csv = pd.Series([movie_record_users_url,movie_record_users_score],columns)
            data=data.append(csv,columns)

            data.to_csv('test2.csv',encoding='utf_8_sig')
        return None