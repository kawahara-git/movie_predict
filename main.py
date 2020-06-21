from Application.user import *
from Application.movie import *

User=User()
Movie=Movie()

def main():
    #ユーザー情報（一時的に固定）
    USER_INFO='ibura11.2'
    #映画タイトル（一時的に固定）
    MOVIE_INFO='ジョーカー'
    #ユーザー情報取得
    user_data,user_movie_urls = User.get_user_data(USER_INFO)
    #映画情報取得
    movie_data,movie_users_urls = Movie.get_movie_data(MOVIE_INFO)
    #映画記録者のユーザー視聴映画情報取得
    user_movie_data = Movie.get_user_movie_data(user_data,user_movie_urls,movie_users_urls)
    #評価予想

if __name__=='__main__':
    main()
