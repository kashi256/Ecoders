
from flask import Flask, render_template, request, redirect, g, url_for
from database import getDatabase, connectToDatabase
import pickle
import numpy as np
filename = 'diabetes-prediction-rfc-model2.pkl'
classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.teardown_appcontext
def closeDatabase(error):
    if hasattr(g, 'diabetes_db'):
        g.diabetes_db.close()


@app.route('/datacollection', methods=["POST", "GET"])
def datacollection():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        pregnancies = int(request.form['pregnancies'])
        mealsperday = int(request.form['mealsperday'])
        totalexersisehours = int ( request.form['totalexersisehours'])
        glucose = int(request.form['glucose'])
        bloodpressure = int(request.form['bloodpressure'])
        skinthickness = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        familyhistory = int(request.form['familyhistory'])
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        db = getDatabase()
        db.execute("insert into persondata (username, age, height, weight, pregnancies, mealsperday, totalexersisehours, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, familyhistory, meal1, meal2, meal3, meal4, meal5 )  values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [username, age, height, weight, pregnancies, mealsperday, totalexersisehours, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, familyhistory, meal1, meal2, meal3, meal4, meal5 ])
        db.commit()
        return redirect(url_for("home"))            
    return render_template("datacollection.html")


@app.route('/bmiresult')
def bmiresult():
    return render_template("bmiresult.html")

@app.route('/glucoseresult')
def glucoseresult():
    return render_template("glucoseresult.html")


@app.route('/bmicalculator', methods = ["POST","GET"])
def bmicalculator():
    bmivalue = 0
    if request.method == "POST":
        height = int(request.form['height'])
        height = height/100
        height = height ** 2
        weight = int(request.form['weight'])
        bmivalue = weight / height
        return render_template('bmiresult.html', bmivalue = bmivalue)
    return render_template("bmicalculator.html", bmivalue = bmivalue)




@app.route('/glucosecalculator', methods = ["POST", "GET"])
def glucosecalculator():
    meal1 = None
    meal2 = None
    meal3 = None
    meal4 = None
    meal5 = None
    glucoseresult = 0
    if request.method == "POST":
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        dict = {"cake" : 47 , 
       "apple" : 44 , 
        "bagel" : 72 , 
        "bun" : 61 , 
        "bread" : 56 , 
        "wheat" : 71 , 
        "floor" : 73 , 
        "grains" : 51 , 
        "coke" : 63 , 
        "fanta" : 68 , 
        "applejuice" : 50 , 
        "orange" : 38 , 
        "tomato" : 55 , 
        "potato" : 61 , 
        "honey" : 58 , 
        "corn" : 55 , 
        "coconut" : 54 , 
        "banana" : 51}

        meals = [meal1, meal2, meal3, meal4, meal5]
        sum = 0
        for i in meals:
            if i in dict.keys():
                sum = sum + dict[i]
                
        glucoseresult = sum / len(meals)



        return render_template("glucoseresult.html", meal1 = meal1, meal2 = meal2, meal3 = meal3, meal4 = meal4, meal5 = meal5, glucoseresult = glucoseresult)
    return render_template("glucosecalculator.html", meal1 = meal1, meal2 = meal2, meal3 = meal3, meal4 = meal4, meal5 = meal5, glucoseresult = glucoseresult)


@app.route("/showcollecteddata", methods = ["POST", "GET"])
def showcollecteddata():
    db = getDatabase()
    db_cur = db.execute("select * from persondata")
    alldata = db_cur.fetchall()
    return render_template("showcollecteddata.html", alldata = alldata)


@app.route('/predict', methods=["POST", "GET"])
def predict():
    prediction_result = None
    recommendedinsulin = None
    recommendedmealsperday = None
    recommendedtotalexersisehours =None
    recommendedglucose = None
    recommendedbloodpressure = None

    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        age = request.form['age']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        pregnancies = int(request.form['pregnancies'])
        mealsperday = int(request.form['mealsperday'])
        totalexersisehours = int ( request.form['totalexersisehours'])
        glucose = float(request.form['glucose'])
        bloodpressure = int(request.form['bloodpressure'])
        skinthickness = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        familyhistory = int(request.form['familyhistory'])
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        if mealsperday < 6 :
            recommendedmealsperday = "Add more meals per day count Should be 6."
        elif mealsperday == 6:
            recommendedmealsperday = "Good keep meals per day count to 6."
        elif  mealsperday > 6:
            recommendedmealsperday = "Reduce meals per day count Should be 6."

        if totalexersisehours < 1 :
            recommendedtotalexersisehours = "Add more exerise hours per day, minimum 1 hour"
        elif totalexersisehours == 1:
            recommendedtotalexersisehours = "keep number of hours in exersize to 1 hour per day.."
        elif totalexersisehours >= 2:
            recommendedtotalexersisehours = "Reduce number of hours in exersize, Try to keep 1 hour/day."

        if glucose < 80 :
            recommendedglucose = "Glucose level needs to be increased. Good Range is (100 to 180)"
        elif glucose >= 80 and glucose <180:
            recommendedglucose  = "Glucose level is maintained. (100 to 180)"
        elif glucose >= 180:
            recommendedglucose  = "Glucose level is high needs to be reduced. Good Range is (100 to 180)"
        
        if bloodpressure < 120 :
            recommendedbloodpressure = "Blood Pressure level needs to be increased. Good Range is (120 to 180)"
        elif bloodpressure >= 120 and bloodpressure <= 180:
            recommendedbloodpressure  = "Blood Pressure level is maintained nicely. Good Range is (120 to 180)"
        elif bloodpressure > 180:
            recommendedbloodpressure  = "Blood Pressure level is high needs to be reduced. Good Range is (120 to 180)"

        
        if insulin < 30 :
            recommendedinsulin = "Insulin level needs to be increased. Good Range is (30 to 846)"
        elif insulin >= 30 and insulin <= 846:
            recommendedinsulin = "Insulin level is Maintained, Good Range is (30 to 846)"
        elif insulin > 846:
            recommendedinsulin = "Insulin level is high needs to be reduced. Good Range is (30 to 846)"


        data = np.array([[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age]])
        prediction_result = classifier.predict(data)
        return render_template('result.html', prediction_result=prediction_result, username = username, meal1 = meal1, meal2 = meal2, meal3 =meal3, meal4 = meal4, meal5= meal5, weight = weight, height = height, glucose = glucose, bloodpressure = bloodpressure, insulin = insulin, totalexersisehours  = totalexersisehours , mealsperday = mealsperday, 
        recommendedmealsperday = recommendedmealsperday,
        recommendedtotalexersisehours = recommendedtotalexersisehours,
        recommendedglucose = recommendedglucose,
        recommendedinsulin = recommendedinsulin,
        recommendedbloodpressure = recommendedbloodpressure)        

    return render_template("predict.html", prediction_result = prediction_result)

if __name__ == '__main__':
	app.run(debug=True)