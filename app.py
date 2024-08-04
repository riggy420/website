from flask import Flask,render_template,request,flash,session,redirect
import library
import time 
import os
import psutil 

from risk_assessment_library_for_new_database import using_risk_assessment as ra
from risk_assessment_library_for_new_database import risk_assessment as database

app = Flask(__name__)   # Flask constructor 
app.secret_key="ldr"
# A decorator used to tell the application 
# which URL is associated function 
# @app.route('/')       
# def hello(): 
#     return render_template('index.html')
  
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

# @app.route('/table')
# def index():
#     return render_template('table.html', title='Analysis Page')


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


@app.route('/', methods=['POST', 'GET'])
def index():
    current_pid = os.getpid()
    process = [p for p in psutil.process_iter() if p.name().lower() in ['python', 'python3']]
    print(process)
    # print(p.pid for p in process)
    print(current_pid)
    print(len(process))
    same_terminal = any(p.pid == current_pid for p in process)
    
    if len(process) >2:
        flash("The script is running in the same terminal.")

    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        a = ra()


        if request.form['btn'] == 'Update_America':    
            if str(ra.getting_latest_date(a,'AAPL','')) != time.strftime("%Y-%m-%d"):
                print("Updating America")
                flash('Updating America. Please wait for a while')

                os.system("python3 ~/Documents/databasecreator.america.py")
                return redirect(request.url)
            else:
                flash('Already updated')
                return redirect(request.url)
        elif request.form['btn'] == 'Update_China':
            if str(ra.getting_latest_date(a,'600600','SS')) != time.strftime("%Y-%m-%d"):
                os.system("python3 ~/Documents/updating_for_china.py")
                flash('Updating China. Please wait for a while')
                return redirect(request.url)
            else:
                flash('Already updated')
                return redirect(request.url)
        elif request.form['btn'] == 'General_Update_in_America':
            with app.app_context():
                print("Struck")
                db.drop_all()
                db.create_all()
                making_data("/home/ricky/Documents/agpd_america_2024-01-26_all_0.001.txt")

            return render_template('table.html', title='Analysis Page')


        else:
            result = request.form
            region = request.form.get("region")
            # getting input with name = lname in HTML form 
            ID = request.form.get("ID")

            context = {
                "function":request.form['btn'],
                "region":region,
                "ID":ID,
                "last_updated":str(ra.getting_latest_date(a,ID,region))
            }

            print("Passed")
            print("Next")
            if ra.what_is_price_when_w_is_fallen_to_20(a,ID,region) == FileNotFoundError:
                flash ("Either StockID or region is wrong")
                return redirect(request.url)

            # b = database(ID,region)


            if request.form['btn'] == 'Searching_for_one': 
                context["result"]=str(ra.finding_one_agpd(a,ID,region))
                return render_template("result.html",len = len(context),context=context)
            elif request.form['btn'] == 'Fall_to_20': 
                print("Here I am")
                # return "<p>" + str(ra.what_is_price_when_w_is_fallen_to_20(a,ID,region)) + "</p>"

                context["result"]=str(ra.what_is_price_when_w_is_fallen_to_20(a,ID,region))
                return render_template("result.html",len = len(context),context=context)
            elif request.form['btn'] == 'Rise_to_40':
                print("Why")

                context["result"],context['result2']=ra.what_is_price_when_w_sell_is_risen_to_40(a,ID,region)
                return render_template("result.html",len = len(context),context=context)
                ## Here is so fucked up => don;t know what happened now
                ## only buggy part -> Keep on returning nonetype object instead of str

            elif request.form['btn'] == 'Reflective_Price':
                if request.form.get("Price") == '': ## If you input nothing -> It crashes 
                    flash("You didn't input price")
                    return redirect(request.url)
                else:
                    price = request.form.get("Price")

                    context["result"]=str(ra.reflective_price(a,ID,region,price))
                    return render_template("result.html",len = len(context),context=context)
            elif request.form['btn'] == 'Price_when_ten_plus_current':
                if request.form.get("W_sell_diff") == '':  ## If you input nothing -> It crashes 
                    flash("You must input W_sell_diff")
                    return redirect(request.url)
                else:
                    W_sell_diff = request.form.get("W_sell_diff")
                    context["result"]=str(ra.what_is_price_when_w_sell_is_risen_to_10_plus_current(a,ID,region,W_sell_diff))

                    return render_template("result.html",len = len(context),context=context) 

    
    return render_template("index.html")

if __name__=='__main__': 
    app.run(host='0.0.0.0' , port=5000,debug=True)


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)