from flask import Flask,render_template,request,flash,session,redirect
import library

from risk_assessment_library_for_new_database import using_risk_assessment as ra 

app = Flask(__name__)   # Flask constructor 
app.secret_key="ldr"
# A decorator used to tell the application 
# which URL is associated function 
# @app.route('/')       
# def hello(): 
#     return render_template('index.html')
  


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        print("Passed")
        result = request.form
        region = request.form.get("region")
    # getting input with name = lname in HTML form 
        ID = request.form.get("ID")
        a = ra()
        print("Next")

        if request.form['btn'] == 'Fall_to_20': 
            print("Here I am")
            # return "<p>" + str(ra.what_is_price_when_w_is_fallen_to_20(a,ID,region)) + "</p>"
            if ra.what_is_price_when_w_is_fallen_to_20(a,ID,region) == FileNotFoundError:
                flash ("Code not found")
                return redirect(request.url)
            context = {
                "function":"Fall_to_20",
                "region":region,
                "ID":ID,
                "result":str(ra.what_is_price_when_w_is_fallen_to_20(a,ID,region))
            }
            return render_template("result.html",len = len(context),context=context)
        elif request.form['btn'] == 'Rise_to_40':
            print("Why")

            return "<p>" + str(ra.what_is_price_when_w_sell_is_risen_to_40(a,ID,region)) + "</p>" 
            ## Here is so fucked up => don;t know what happened now
            ## only buggy part -> Keep on returning nonetype object instead of str

        elif request.form['btn'] == 'Reflective_Price':
            if request.form.get("Price") == '': ## If you input nothing -> It crashes 
                flash("You didn't input price")
                return redirect(request.url)
            else:
                price = request.form.get("Price")
            
                context = {
                    "function":"Reflective_Price",
                    "region":region,
                    "ID":ID,
                    "Price":price,
                    "result":str(ra.reflective_price(a,ID,region,price))
                }
                return render_template("result.html",len = len(context),context=context)
        elif request.form['btn'] == 'Price_when_ten_plus_current':
            if request.form.get("W_sell_diff") == '':  ## If you input nothing -> It crashes 
                flash("You must input W_sell_diff")
                return redirect(request.url)
            else:
                W_sell_diff = request.form.get("W_sell_diff")
                context = {
                    "function":"Price_when_W_sell_different_plus_current",
                    "region":region,
                    "ID":ID,
                    "W_sell_diff":W_sell_diff,
                    "result":str(ra.what_is_price_when_w_sell_is_risen_to_10_plus_current(a,ID,region,W_sell_diff))
                }
                return render_template("result.html",len = len(context),context=context)            
    
    return render_template("index.html")

if __name__=='__main__': 
    app.run(host='0.0.0.0' , port=5000,debug=True)


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)