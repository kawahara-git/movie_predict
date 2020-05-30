from user import *

User=User()

def main():
    #ベースのURL（フィルマークス）
    BASE_URL='https://filmarks.com/'    
    #ユーザーのURL
    USER_URL='users/'
    #ユーザー情報（一時的に固定）
    USER_INFO='ibura11.2'
    #映画タイトル（一時的に固定）
    #MOVIE_TITLE='ジョーカー'
    #ユーザー情報取得
    User.get_user_data(BASE_URL,USER_URL,USER_INFO)
    #映画の評価情報取得

    #前処理

    #評価予想


if __name__=='__main__':
    main()