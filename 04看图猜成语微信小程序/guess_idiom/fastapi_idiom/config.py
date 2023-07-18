class Config:
    SECRET_KEY = 'mrsoft'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysql80@localhost/idiom?charset=utf8mb4"

    # 小程序配置信息
    AppID = 'wx994e6f48ed740108'     # 小程序的AppID
    AppSecret = 'bd982c8659d2c60e99a4fc73dfca65f6' # 小程序的AppSecret