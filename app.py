from flask import Flask, render_template,request
 
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html', name = "Nehal")
 
@app.route('/about')
def about():
    return render_template('about.html', discription = """I am a student in Integrated AI.
I am from India.
Also I am too lazy to think about anything else!""")

@app.route("/greet",methods = ["GET", "POST"])
def greet():
    if request.method == "POST":
        name = request.form["name"]
        return render_template("greet_result.html",name =name)
    return render_template("greet_form.html")

@app.route("/bmi",methods = ["GET", "POST"])
def bmi():
    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])/ 100
        bmi_value = round(weight/(height**2),1)
 
        if bmi_value <18.5:
            category = "Underweight"
        elif bmi_value < 25:
            category = "Normal weight"
        elif bmi_value < 30:
            category = "Overweight"
        else:
            category = "Obese"
 
        return render_template("bmi_result.html",weight =weight, height = float(request.form["height"]), bmi = bmi_value, category= category)
    return render_template("bmi_form.html") 

@app.route("/grade",methods = ["GET", "POST"])
def grade():
    if request.method == "POST":
        name = str(request.form["name"])
        grade = float(request.form["grade"])
 
        if grade >= 90 :
            Gradecategory = "A"
        elif grade >= 80:
            Gradecategory = "B"
        elif grade >= 70:
            Gradecategory = "C"
        elif grade >= 60:
            Gradecategory = "D"
        else:
            Gradecategory = "F"
 
        return render_template("grade_result.html", name = name, grade = grade, GradeChecker = Gradecategory)
    return render_template("grade_form.html")  

 
if __name__ == '__main__':
    app.run(debug=True)