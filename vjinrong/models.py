from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request



class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(45), unique=True, nullable=False)
    _password = db.Column(db.String(255))
    rec_num = db.Column(db.String(24))
    bound_wechat = db.Column(db.String(45))
    reister_time = db.Column(db.DateTime, default=datetime.now)
    ip = db.Column(db.String(45), nullable=False)
    isban = db.Column(db.SmallInteger, default=0)

    # 外键关联
    file = db.relationship('LoanFile', backref='company', lazy='dynamic')  # 关联融资文件表
    info = db.relationship('CompanyInfo', backref='company', lazy='dynamic')  # 关联企业资料表
    apply = db.relationship('LoanApply', backref='company', lazy='dynamic')  # 关联融资申请表
    score = db.relationship('Score', backref='company', lazy='dynamic')  # 关联企业评分表
    subscribe = db.relationship('Subscribe', backref='company', lazy='dynamic')  # 关联产品收藏表
    cancelling_stocks = db.relationship('CancellingStocks', backref='company', lazy='dynamic')  #

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_phone(account, secret):
        with db.auto_commit():
            company = Company()
            company.phone = account
            company.password = secret
            company.ip = request.remote_addr
            db.session.add(company)

    @staticmethod
    def changePhone(uid, new_phone):
        with db.auto_commit():
            company = Company.query.filter_by(id=uid).first()
            company.phone = new_phone

    @staticmethod
    def resetPassword(account, secret):
        with db.auto_commit():
            company = Company.query.filter_by(phone=account).first()
            company.password = secret


    def check_password(self, raw):
        return check_password_hash(self._password, raw)


class Bank(db.Model):
    __tablename__ = 'bank_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24), nullable=False)
    phone = db.Column(db.String(45), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    section = db.Column(db.String(45), nullable=False) # 所属银行，机构
    rank = db.Column(db.SmallInteger,nullable=False)  # 管理员权限等级，1：代表受理人员，2：代表审批人员，3：管理员（权限最高）
    rec_num = db.Column(db.SmallInteger, unique=True)  # 推荐码
    register_time = db.Column(db.DateTime, default=datetime.now)
    ip = db.Column(db.String(45))
    # 外键
    # apply = db.relationship('LoanApply', backref='bank_user', lazy='dynamic')
    product = db.relationship('Product',backref='bank_user',lazy='dynamic')
    contract_template = db.relationship('ContractTemplate',backref='bank_user',lazy='dynamic')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_phone(account, secret):
        with db.auto_commit():
            bank = Bank()
            bank.phone = account
            bank.password = secret
            db.session.add(bank)

    # @staticmethod
    # def verify(phone, password):
    #     bank = Bank.query.filter_by(phone).first()
    #     if not bank.check_password(password):
    #         raise AuthFailed
    #     return {'uid': bank.id}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


# 企业资料表
class CompanyInfo(db.Model):
    __tablename__ = 'company_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    sid = db.Column(db.String(24), nullable=False) # e签宝实名认证服务号后6位
    service_id = db.Column(db.String(45), nullable=False) # e签宝实名认证服务号
    remit_sum = db.Column(db.String(45),nullable=False)  #  打款金额
    tax_rank = db.Column(db.String(45))  # 该企业的退税等级
    company_name = db.Column(db.String(100), nullable=False)
    company_type = db.Column(db.String(45), nullable=False)
    province = db.Column(db.String(24), nullable=False)
    city = db.Column(db.String(24), nullable=False)
    bankName = db.Column(db.String(128), nullable=False)
    subBankName = db.Column(db.String(128), nullable=False)
    bankNo = db.Column(db.String(45), nullable=False)
    legalPersonName = db.Column(db.String(24), nullable=False)
    linkName = db.Column(db.String(24), nullable=False)
    linkPhone = db.Column(db.String(24), nullable=False)
    licenseNo = db.Column(db.String(45), unique=True, nullable=False)
    idCardNo = db.Column(db.String(45), nullable=False)
    realNameVerify = db.Column(db.SmallInteger, default=1) # e签宝实名认证 1：未认证，2：待认证，3：已认证

    # 以下字段为企业外部数据(未知数据来源)
    cofoundTime = db.Column(db.String(128)) # 企业成立时间
    productType = db.Column(db.String(45)) # 出口产品品类
    retaxFirstYear = db.Column(db.String(128)) # 初始退税年份
    nationalTaxRegister = db.Column(db.String(128
                                              )) # 国税注册年份
    recentRetaxAmount = db.Column(db.String(45))
    supplyProvince = db.Column(db.String(24))

    product = db.relationship('Score',backref='company_info',lazy='dynamic')  # 关联企业评分表
    cancelling_stocks = db.relationship('CancellingStocks',backref='company_info',lazy='dynamic')  # 关联企业退税记录表


    def to_info_dict(self):
        """将企业基本信息转为字典"""
        company_dict = {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "company_type": self.company_type,
            "province": self.province,
            "city": self.city,
            "bankName": self.bankName,
            "subBankName": self.subBankName,
            "bankNo": self.bankNo,
            "legalPersonName": self.legalPersonName,
            "linkName": self.linkName,
            "linkPhone": self.linkPhone,
            "licenseNo": self.licenseNo,
            "idCardNo": self.idCardNo
        }

        return company_dict


# 产品表
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_user_id = db.Column(db.Integer, db.ForeignKey("bank_user.id"))
    name = db.Column(db.String(24),nullable=False)
    fund = db.Column(db.String(45),nullable=False)  #  产品所属机构
    privilegeId = db.Column(db.Integer) # 特权id, 产品在列表中顺序
    maxAmount = db.Column(db.Float) # 最高额度
    rate = db.Column(db.Float) # 融资利率
    term = db.Column(db.Integer) # 融资期限
    fundUrl = db.Column(db.String(255)) # 资金方产品的链接
    online = db.Column(db.SmallInteger, default=1)  # 0下架, 1上线

    file_name = db.Column(db.String(255))  #  产品融资申请需要的材料文件名
    accessDetails = db.Column(db.String(255)) # 准入条件详情
    creditAmount = db.Column(db.String(255)) # 授信额度详情
    guaranteeMeasure = db.Column(db.String(255)) # 担保措施
    LoanTime = db.Column(db.String(255)) # 放款时间点
    repayment = db.Column(db.String(255)) # 还款方式
    serviceFee = db.Column(db.String(255)) # 平台服务费描述
    serviceFeeDetail = db.Column(db.String(255)) # 平台服务费详细介绍

    # 产品特点
    productStyle = db.Column(db.String(255))

    # 产品简介图片
    productInfo = db.Column(db.String(255))

    subscribe = db.relationship('Subscribe', backref='product', lazy='dynamic')  # 关联产品收藏表
    loan_apply = db.relationship('LoanApply', backref='product', lazy='dynamic')  # 关联融资申请表
    contract_template = db.relationship('ContractTemplate', backref='product', lazy='dynamic')  # 关联融资产品合同模板表



    def to_basic_dict(self):
        """将产品基本信息转为字典数据"""
        product_dict = {
            "id": self.id,
            "fund": self.fund,
            "name": self.name,
            "productStyle1": self.productStyle1,
            "productStyle2": self.productStyle2,
            "productStyle3": self.productStyle3,
            "rate": self.rate,
            "term": self.term,
            "productInfo1": self.productInfo1,
            "maxAmount": self.maxAmount
        }
        return product_dict

    def to_full_dict(self):
        """将产品详细信息转为字典"""
        products_dict = {
            "name": self.name,
            "rate": self.rate,
            "maxAmount": self.maxAmount,
            "term": self.term,
            "accessDetails": self.accessDetails,
            "creditAmount": self.creditAmount,
            "guaranteeMeasure": self.guaranteeMeasure,
            "loanTime": self.LoanTime,
            "serviceFee": self.serviceFee,
            "repayment": self.repayment
        }
        return products_dict


#  融资产品合同模板表
class ContractTemplate(db.Model):
    __tablename__ = 'contract_template'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'), nullable=False)
    bank_id = db.Column(db.Integer,db.ForeignKey('bank_user.id'),nullable=False)
    contrat_name = db.Column(db.String(128),nullable=False)
    contract_file_url = db.Column(db.String(128),nullable=False)
    upload_time = db.Column(db.DateTime,default=datetime.now)


# 融资申请订单表
class LoanApply(db.Model):
    __tablename__ = 'loanapply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),nullable=False)
    # bank_user_id = db.Column(db.Integer, db.ForeignKey('bank_user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    order_id = db.Column(db.String(128), unique=True, nullable=False)  # 订单号
    rec_num = db.Column(db.SmallInteger)  # 推荐码
    section = db.Column(db.String(45),nullable=False)  #  融资订单产品所属的机构
    company_name = db.Column(db.String(45),nullable=False)  # 融资订单所在的企业名称
    product_name = db.Column(db.String(45),nullable=False)  # 申请融资产品的名称
    applyTime = db.Column(db.DateTime, default=datetime.now)
    isFinish = db.Column(db.SmallInteger, default=0) # 0没完成， 1 完成

    # 调用我们数据接口
    retaxId = db.Column(db.String(45))
    retaxDate = db.Column(db.String(24)) # 由于退税数据是年月：201804, 目前以字符串形式存储
    retaxPc = db.Column(db.String(24))
    retaxAmount = db.Column(db.Float)

    applyAmount = db.Column(db.Float)
    grantDate = db.Column(db.Date)
    dateline = db.Column(db.Date)

    interest = db.Column(db.Float) # 利息
    status = db.Column(db.SmallInteger, default=0) # 0代表待受理
    acceptTime = db.Column(db.DateTime) # 受理时间

    reviewTime = db.Column(db.DateTime, default=datetime.now) # 审批时间

    loanAmount = db.Column(db.Float) # 发放融资金额
    loanRate = db.Column(db.Float) # 融资利率
    loanTerm = db.Column(db.Date)

    riskTime = db.Column(db.DateTime, default=datetime.now)

    rejectReason = db.Column(db.String(255)) # 拒绝原因
    reviewOpinion = db.Column(db.Text)# 审批意见


    # reviewPersonId = db.Column(db.Integer, db.ForeignKey('bank_user.id')) # 审批人员
    loan_file = db.relationship('LoanFile',backref='loanapply', lazy='dynamic')  # 关联融资申请订单文件表


# 融资申请订单文件表
class LoanFile(db.Model):
    __tablename__ = 'loan_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    apply_id = db.Column(db.Integer, db.ForeignKey('loanapply.id'), nullable=False)

    # 融资订单上传的文件
    file_name = db.Column(db.String(64), nullable=False)
    file_url = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128))  # 融资文件状态，通过为0，每通过为-1
    reason = db.Column(db.String(256))  # 当文件未通过时，说明未通过的原因
    upload_time = db.Column(db.DateTime,default=datetime.now)


# 企业评分表
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company_info_id = db.Column(db.Integer, db.ForeignKey('company_info.id'), nullable=False)
    level = db.Column(db.String(24)) # 退税等级

    # 评分
    license_num = db.Column(db.String(64))  # 营业执照注册号
    abilityScore = db.Column(db.Integer)
    riskScore= db.Column(db.Integer)
    creditScore = db.Column(db.Integer)
    repayAbilityScore = db.Column(db.Integer)
    legalScore = db.Column(db.Integer)
    repayWillingScore = db.Column(db.Integer)
    updateTime = db.Column(db.DateTime, default=datetime.now)


# 产品收藏表
class Subscribe(db.Model):
    __tablename__ = 'subscribe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    subTime = db.Column(db.DateTime, default=datetime.now)


# 用户企业退税记录表
class CancellingStocks(db.Model):
    __tablename__ = 'cancelling_stocks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'), nullable=False)
    company_info_id = db.Column(db.Integer,db.ForeignKey('company_info.id'), nullable=False)
    canselling_time = db.Column(db.String(128),nullable=False)  # 退库所属时间
    batch_num = db.Column(db.String(128),nullable=False)  # 批次号码
    canselling_bank = db.Column(db.String(128),nullable=False)  # 退库银行
    canseliing_id = db.Column(db.String(128),nullable=False)  # 退库账号
    add_value_tax = db.Column(db.String(128),nullable=False)  # 增值税额
    k_mark = db.Column(db.String(128),nullable=False)  # 金三退库标志
    k_time = db.Column(db.String(128),nullable=False)  # 金三退库时间
    t_mark = db.Column(db.String(128),nullable=False)  # 退税标志
    t_time = db.Column(db.String(128),nullable=False)  # 退税时间





