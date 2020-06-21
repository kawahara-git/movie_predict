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

class Movie:
    #タイトル検索から検索結果を取得
    def get_movie_search_url(self,movie_title):
        #検索結果URLの生成
        search_root_front='search/movies?'
        search_root_end='&view=rich'
        search_title='q='+movie_title
        search_url = BASE_URL +search_root_front+search_title+search_root_end
        return search_url
    def get_movie_url(self,movie_title):
        movie_search_url=Movie.get_movie_search_url(self,movie_title)
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
    #検索映画記録データ取得
    def get_movie_data(self,movie_title):
        print("***** 映画情報取得開始 *****")
        #映画の情報取得
        movie_url = Movie.get_movie_url(self,movie_title)
        movie_soup = Scraping.generate_bs_object(movie_url)
        #映画視聴者情報取得
        movie_record_users=Scraping.get_class_info(movie_soup,'c-media')
        #映画視聴者URLと視聴者スコア取得
        movie_record_users_urls=re.findall('"/users/(.*?)"',str(movie_record_users))
        movie_record_users_scores=re.findall('<div class="c-rating__score">(\d+\.\d|-)',str(movie_record_users))
        #データフレーム作成
        data=pd.DataFrame({'Title':[movie_title]})
        movie_record_user_num = len(movie_record_users)
        print("対象ユーザー数："+str(movie_record_user_num))
        for i in range(movie_record_user_num):
            #URL取得
            # movie_record_users_url = movie_record_users_urls[i]
            # movie_record_users_url = BASE_URL + movie_record_users_url
            #スコア取得
            data['User'+str(i+1)+'Score'] = movie_record_users_scores[i]
        data=data.set_index('Title')
        data.to_csv('test2.csv',encoding='utf_8_sig')
        print("***** 映画情報取得完了 *****")
        return data, movie_record_users_urls


    #映画データ取得
    def get_user_movie_data(self,user_data,user_movie_urls,movie_users_urls):
        print("***** 映画記録者のユーザー視聴映画情報取得開始 *****")
        #ユーザー映画の平均値取得
        avg_scores = Scraping.get_avg_score(user_movie_urls)
        #映画記録者のユーザー視聴映画データ作成
        #ユーザー映画情報取得
        columns=['Title']
        data=pd.DataFrame(columns=columns)
        data['Title'] = user_data['Title']
        #共通項で表埋め

        #欠損値埋め
        
        data=data.set_index('Title')
        data.to_csv('test4.csv',encoding='utf_8_sig')
        print("***** 映画記録者のユーザー視聴映画情報取得完了 *****")
        return data
        # #映画の情報取得
        # movie_url = Movie.get_movie_url(self,movie_title)
        # movie_soup = Scraping.generate_bs_object(movie_url)
        # #映画視聴者情報取得
        # movie_record_users=Scraping.get_class_info(movie_soup,'c-media')
        # #映画視聴者URLと視聴者スコア取得
        # movie_record_users_urls=re.findall('"/users/(.*?)"',str(movie_record_users))
        # movie_record_users_scores=re.findall('<div class="c-rating__score">(\d+\.\d|-)',str(movie_record_users))
        # #データフレーム作成
        # data=pd.DataFrame({'Title':[movie_title]})
        # movie_record_user_num = len(movie_record_users)
        # print("対象ユーザー数："+str(movie_record_user_num))
        # for i in range(movie_record_user_num):
        #     #URL取得
        #     # movie_record_users_url = movie_record_users_urls[i]
        #     # movie_record_users_url = BASE_URL + movie_record_users_url
        #     #スコア取得
        #     data['User'+str(i+1)+'Score'] = movie_record_users_scores[i]
        # data=data.set_index('Title')
