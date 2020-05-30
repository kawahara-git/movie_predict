import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

class User:
    #指定クラス情報取得
    def get_class_info(self,soup,class_name):
        info=soup.find_all(class_=class_name)
        return info
    #指定URL1ページの情報取得
    def generate_bs_object(self,movie_url,page=1):
        info=requests.get(movie_url,params={"page":page})
        status_code=info.status_code
        if status_code != 200:
            contents=None
        else:
            contents=BeautifulSoup(info.content,'lxml')
            time.sleep(1)
        return contents
    #平均スコア取得
    def get_avg_score(self,url):
        soup=User.generate_bs_object(self,url)
        score_info=User.get_class_info(self,soup,'c-rating__score')
        avg_score=score_info[0].text    
        return avg_score
    def get_user_data(self,BASE_URL,USER_URL,USER_INFO):
        #1.ユーザーURLの取得###################################
        user_url=BASE_URL + USER_URL + USER_INFO 
        #2.ユーザーURLにアクセス###################################
        #ユーザーの情報取得
        user_soup=User.generate_bs_object(self,user_url)
        if user_soup==None:
            print('アクセスエラー')
        else:
            #タイトルとユーザースコアと平均スコア取得
            titles=User.get_class_info(self,user_soup,'c-content-card__title')
            user_scores=User.get_class_info(self,user_soup,'c-rating__score')
            urls=User.get_class_info(self,user_soup,'c-content__jacket')
            #データフレーム作成
            columns=['Title','user_Score','avg_Score']
            user_data=pd.DataFrame([USER_INFO,'',''])
            data=pd.DataFrame(columns=columns)
            for i in range(len(titles)):
                #タイトル取得
                title_all=titles[i].a.text
                title_year=titles[i].span.text
                title=title_all.replace(title_year,'').strip()
                #ユーザースコア取得
                user_score=user_scores[i].text
                #映画URLの生成
                movie_url=urls[i].get('href')
                #root='https://filmarks.com/'
                movie_url = BASE_URL + movie_url
                #平均スコア取得
                avg_score=User.get_avg_score(self,movie_url)
                csv = pd.Series([title,user_score,avg_score],columns)
                data=data.append(csv,columns)
            data=data.set_index('Title')
            
            data= pd.concat([user_data,data],axis=0)
            
            data.to_csv('test.csv',encoding='utf_8_sig')
        return None
