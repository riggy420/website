from flask import Flask,render_template,request,flash,session,redirect,make_response,jsonify
import time 
import json
import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    stockid = db.Column(db.String(64), primary_key=True)
    agpd_value = db.Column(db.Float, index=True)
    current_price = db.Column(db.Float, index=True)
    number_of_trade = db.Column(db.Float)
    w_buy = db.Column(db.Float)
    w_sell = db.Column(db.Float)
    day_last_update = db.Column(db.String(64))
    average_day = db.Column(db.Float)
    day_standard_deviation = db.Column(db.Float)
    W_moderate_diff = db.Column(db.Float)
    five_day_average = db.Column(db.Float)


    def to_dict(self):
        return {
            'stockid': self.stockid,
            'agpd_value': self.agpd_value,  
            'current_price': self.current_price,
            'number_of_trade': self.number_of_trade,
            'w_buy': self.w_buy,
            'w_sell': self.w_sell,
            'day_last_update': self.day_last_update,
            'average_day': self.average_day,
            'day_standard_deviation': self.day_standard_deviation,
            'W_moderate_diff': self.W_moderate_diff,
            'five_day_average': self.five_day_average
        }



def making_data(filename):
    print("Here")
    with open(filename,'r') as f:
        print("Here")
        for line in f:
            if (line[0:4] == "Stoc"):
                continue
            
            stockid,agpd_value,current_price,number_of_trade,w_buy,w_sell,day_last_update,average_day,day_standard_deviation,W_moderate_diff,five_day_average = line.strip().split(' ')

            user = User(
                stockid=stockid, 
                agpd_value=float(agpd_value), 
                current_price=float(current_price), 
                number_of_trade=int(number_of_trade), 
                w_buy=float(w_buy), 
                w_sell=float(w_sell), 
                day_last_update=day_last_update, 
                average_day=float(average_day), 
                day_standard_deviation=float(day_standard_deviation), 
                W_moderate_diff=float(W_moderate_diff), 
                five_day_average=float(five_day_average)
                )
            
            db.session.add(user)
        db.session.commit()

# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template('table.html', title='Analysis Page')


@app.route('/api/data')
def data():
    query = User.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.stockid.like(f'%{search}%'),
            User.agpd_value.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['stockid', 'agpd_value','number_of_trade','w_buy']:
            col_name = 'stockid'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


# class TableServer:
#     def __init__(self,name):
#         self.app = Flask(name)

#         @self.app.route('/table')
#         def __index():
#             return self.index()
        
#         @self.app.route('/api/data')
#         def __data():
#             return self.data()
    
#     def index(self):
#         return render_template('table.html', title='Analysis Page')
    
#     def data(self):
#         query = User.query

#         # search filter
#         search = request.args.get('search[value]')
#         if search:
#             query = query.filter(db.or_(
#                 User.stockid.like(f'%{search}%'),
#                 User.agpd_value.like(f'%{search}%')
#             ))
#         total_filtered = query.count()

#         # sorting
#         order = []
#         i = 0
#         while True:
#             col_index = request.args.get(f'order[{i}][column]')
#             if col_index is None:
#                 break
#             col_name = request.args.get(f'columns[{col_index}][data]')
#             if col_name not in ['stockid', 'agpd_value','number_of_trade','w_buy']:
#                 col_name = 'stockid'
#             descending = request.args.get(f'order[{i}][dir]') == 'desc'
#             col = getattr(User, col_name)
#             if descending:
#                 col = col.desc()
#             order.append(col)
#             i += 1
#         if order:
#             query = query.order_by(*order)

#         # pagination
#         start = request.args.get('start', type=int)
#         length = request.args.get('length', type=int)
#         query = query.offset(start).limit(length)

#         # response
#         return {
#             'data': [user.to_dict() for user in query],
#             'recordsFiltered': total_filtered,
#             'recordsTotal': User.query.count(),
#             'draw': request.args.get('draw', type=int),
#         }
    
#     def run(self,host,port,debug,filename):
#         with app.app_context():

#             db.drop_all()
#             db.create_all()
#             making_data(filename)

#             self.app.run(host=host,port=port,debug=debug)
    



if __name__ == '__main__':
    # server = TableServer(__name__)
    # server.run(host="0.0.0.0",port=5000,debug=True,filename="/home/ricky/Documents/agpd_america_2024-01-26_all_0.001.txt")
    with app.app_context():
        print("Here")
        db.drop_all()
        db.create_all()
        making_data("/home/ricky/Documents/agpd_america_2024-01-26_all_0.001.txt")

        app.run(debug=True)