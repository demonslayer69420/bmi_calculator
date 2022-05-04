from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:884971@localhost/BMI-calculator'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(255), unique=True)
    name_=db.Column(db.String(255))
    weight_=db.Column(db.Float(2))
    height_=db.Column(db.Integer)
    bmi_=db.Column(db.Float(1))

    def __init__(self, email_, name_, weight_, height_, bmi_):
        self.email_=email_
        self.name_=name_
        self.weight_=weight_
        self.height_=height_
        self.bmi_=bmi_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email = request.form["email"]
        name = request.form["name"]
        weight = request.form["weight"]
        height = request.form["height"]
        
        bmi_= round(float(weight)/(((float(height)/100)**2)),1)
        print(email, height)
        if db.session.query(Data).filter(Data.email_ == email).count()== 0:
            data=Data(email,name, weight, height, bmi_)
            db.session.add(data)
            db.session.commit()
            average_weight=db.session.query(func.avg(Data.weight_)).scalar()
            average_weight=round(average_weight, 1)
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, weight, average_weight, height, average_height, count, bmi_)
            print(average_height)
            return render_template("success.html")
    return render_template('index.html', text="Seems like we got something from that email once!")

if __name__ == '__main__':
    app.debug=True
    app.run(port=5005)
