from . import passport_blue
from vjinrong.models import Bank
from flask import request,jsonify
from flask import session

@passport_blue.route("/login",methods=["POST"])
def login():
    mobile = request.json.get("mobile")
    password = request.json.get("password")

    bank_user = Bank.query.filter(Bank.mobile == mobile).first()

    if not bank_user:
        return jsonify(error_code = 0,msg = "用户不存在")

    if not bank_user.check_password(password):
        return jsonify(error_code = 0,msg = "请输入正确的密码")

    session["user_id"] = bank_user.id


    rank_num = bank_user.rank
    data = {"rank":rank_num,"name":bank_user.name}
    return jsonify(error_code = 1,msg = "登陆成功",data = data)
