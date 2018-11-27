from flask import Flask
from config import config_map, DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis



redis_store = None # type:redis.StrictRedis
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 在不动当前代码的同时,修改config类的名字
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    db.init_app(app)
    global redis_store
    # 初始化redis的存储数据对象(短信验证码,图片验证码)
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,port=config_class.REDIS_PORT,decode_responses=True)

    Session(app)

    from vjinrong.passport import passport_blue
    app.register_blueprint(passport_blue)

    return app