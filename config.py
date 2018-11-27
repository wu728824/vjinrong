import redis

class Config(object):

    SECRET_KEY = "jdlakdjflkasdjflaskflaase#fgs"

    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/vjinrong"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ip地址
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 设置数据库的类型
    SESSION_TYPE = "redis"
    # 表示session两天之后过期
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 把flasksession放置到redis数据库当中
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development":DevelopmentConfig,  # 开发模式
    "production":ProductionConfig  # 线上模式
}

