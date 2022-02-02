from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, login, email, date, balance, password):
        self.name = name
        self.login = login
        self.email = email
        self.date = date
        self.balance = balance
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not login or not password:
            return None

        user = cls.query.filter_by(login=login).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)



class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False)

    def __init__(self, servise, price, status):
        self.service = servise
        self.price = price
        self.status = status

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200), nullable=False)
    service = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, date, service, price, balance):
        self.date = date
        self.service = service
        self.price = price
        self.balance = balance



class Payments(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200), nullable=False)
    service = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __init__(self, date, service, price, status):
        self.date = date
        self.service = service
        self.price = price
        self.status = status

    def update(cls, **new_data):
        try:
            print(new_data)
            query = cls.query().filter_by(id == new_data.get('id')).first()
            query.description = [new_data.get('id'),
                                 new_data.get('service'),
                                 new_data.get('price'),
                                 new_data.get('Оплачено')]
            cls.session.commit()
        except:
            cls.session.rollback()
            return {'error': 'error'}
        return True

    def get_pay(cls, **kwargs):
        id = kwargs.get('id')

        if not id:
            return None

        pay = cls.query.filter_by(id=id).first()

        return pay





