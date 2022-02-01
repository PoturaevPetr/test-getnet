from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from flask_login import LoginManager, login_user, login_required
#from cache import *
from UserLogin import UserLogin
from flask_mail import Mail, Message
from models import *
from flask_migrate import Migrate
import json
import pdfkit

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'ahahahaha'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///getnet"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'getnet107@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'getnet107@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'tonimo83'  # введите пароль




db = SQLAlchemy(app)
migrate = Migrate(app, db)


CORS(app)


login_manager = LoginManager()
login_manager.init_app(app)


mail = Mail(app)


USER = []


@app.route("/Register", methods=["GET", "POST"])
def register():
    response_object = {"status": "susses"}


    if request.method == "POST":
        post_data = request.get_json()
        user = {
            'name': post_data.get('name'),
            'login': post_data.get('login'),
            'email': post_data.get('email'),
            'password': post_data.get('password1')
        }
        if not User.query.filter_by(email=post_data.get('email')).all():

            new_user = User(name=post_data.get('name'),
                              login=post_data.get('login'),
                              email=post_data.get('email'),
                              date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                              balance=50000,
                              password=post_data.get('password1'))
            db.session.add(new_user)
            db.session.commit()
        else:
            response_object["message"] = "Пользователь уже зарегистрирован"
    return jsonify(response_object)

@app.route('/Login', methods=["GET", "POST"])
def login():
    response_object = {"status": "susses"}
    post_data = request.get_json()
    if request.method == "POST":
        user = User.authenticate(**post_data)
        if user != None:
            userLogin = UserLogin().created(user)
            login_user(userLogin, remember=post_data.get("remember"))
            db_user = UserLogin().User(user)
            USER.append(
                {
                    "id": db_user.id,
                    "name": db_user.name,
                    "email": db_user.email,
                    "register": db_user.date,
                    "balance": db_user.balance,
                }
            )

        else:
            response_object['message'] = "Неверные логин или пароль"
    return jsonify(response_object)

@login_manager.user_loader
def getUser(id_user):
    print('dfvsfb')
    return UserLogin().initDB(id_user, User)

@app.route('/user', methods=['GET'])
def initUser():
    response_object = {"status": "susses"}
    user = UserLogin
    response_object['data_user'] = USER[0]

    return jsonify(response_object)

@app.route('/history', methods=['GET'])
def getHistory():
    response_object = {"status": "susses"}
    data = History.query.all()
    history = []
    for hist in data:
        history.append(
            {
                "id": hist.id,
                "date": hist.date,
                "service": hist.service,
                "price": hist.price,
                "balance": hist.balance
            }
        )
    response_object['data_history'] = history
    return jsonify(response_object)

@app.route('/payments', methods=['GET', 'POST'])
def getPayments():
    response_object = {"status": "susses"}
    if request.method == 'POST':
        post_data = request.get_json()

        USER[0]['balance'] = USER[0]["balance"]-post_data.get("price")

        User.query.filter_by(id=USER[0]['id']).all().update({"balance": USER[0]['balance']})

        new_history = History(date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                              service=post_data.get("service"),
                              price=post_data.get("price"),
                              balance=USER[0]["balance"])######дописать
        db.session.add(new_history)
        db.session.commit()

        Payments.update(post_data)
        if Payments.get_pay(post_data) != None:
            new_payment = Payments(date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                   service=post_data.get('service'),
                                   price=post_data.get('price'),
                                   status='Оплачено')
            db.session.add(new_payment)
            db.session.commit()

    else:
        data = Payments.query.all()
        payments = []
        for pay in data:
            payments.append(
                {
                    "id": pay.id,
                    "data": pay.date,
                    "service": pay.service,
                    "price": pay.price,
                    "status": pay.status,
                }
            )
        response_object['data_payments'] = payments
    return jsonify(response_object)

@app.route('/services', methods=['GET', 'POST'])
def getServices():
    response_object = {"status": "susses"}
    if request.method == 'POST':
        post_data = request.get_json()
        #User.query.filter_by(id=USER[0]['id']).update({"balance": USER[0]['balance']})
        if post_data.get('status') == 'Отключена':
            USER[0]['balance'] = USER[0]["balance"] - post_data.get("price")


            new_history = History(date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                  service=post_data.get("service"),
                                  price=post_data.get("price"),
                                  balance=USER[0]["balance"])
            db.session.add(new_history)



            new_payment = Payments(date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                   service=post_data.get('service'),
                                   price=post_data.get('price'),
                                   status="Оплачено")
            db.session.add(new_payment)
            db.session.commit()

            Service.query.filter_by(id=USER[0]['id']).update({"status": "Подключена"})
        else:
            Service.query.filter_by(id=USER[0]['id']).update({"status": "Отключена"})
    else:
        Service.query.all()
        service = [{"id": serv.id, "service": serv.service, "price": serv.price, "status": serv.status} for serv in Service.query.all()]

        response_object['data_services'] = service

    return jsonify(response_object)

#дописать
@app.route('/sendDetails', methods=['GET', 'POST'])
def sendEmail():
    response_object = {'status': 'susses'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)

        data = [{'date': hist.date, 'service': hist.service, 'price': hist.price, 'balance': hist.balance} for hist in History.query.all()]
        msg = Message(str(data), recipients=[post_data.get('email')])
        msg.body = "Example"
        mail.send(msg)
    return jsonify(response_object)

@app.route('/exit', methods=['GET'])
def exitUser():
    response_object = {"status": "susses"}
    USER.clear()
    return jsonify(response_object)

if __name__ == "__main__":
    app.run(debug=True)
