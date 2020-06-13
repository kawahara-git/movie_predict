from Application.user import *
from Application.movie import *

User=User()
Movie=Movie()

def main():
    #ベースのURL（フィルマークス）
    BASE_URL='https://filmarks.com/'
    #ユーザー情報（一時的に固定）
    USER_INFO='ibura11.2'
    #映画タイトル（一時的に固定）
    MOVIE_INFO='ジョーカー'
    #ユーザー情報取得
    User.get_user_data(BASE_URL,USER_INFO)
    #映画の評価情報取得
    Movie.get_movie_data(BASE_URL,MOVIE_INFO)
    #評価予想


if __name__=='__main__':
    main()
