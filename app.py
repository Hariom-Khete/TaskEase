from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///errands.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class errands(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    job = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    pay = db.Column(db.Integer , nullable = False)
    date_created = db.Column(db.Date,default = datetime.now().date())

    def __repr__(self) -> str :
        return f'S.no :  {self.sno} , Title :  {self.job}'


@app.route("/", methods = ['GET','POST'])
def TaskEase():
    if request.method=='POST':
        job = request.form['title']
        desc = request.form['desc']
        pay = request.form['pay']
        job = errands(job = job, desc = desc , pay = pay)
        db.session.add(job)
        db.session.commit()
    alljobs = errands.query.all()
    print(alljobs)
    return render_template("index.html" , alljobs = alljobs)


@app.route("/About")
def about():
    return render_template('about.html')


@app.route("/all_jobs")
def all_jobs():
    alljobs = errands.query.all()
    print(alljobs)
    return "<p>this is jobs page!</p>"


@app.route('/remove/<int:sno>')
def remove(sno):
    job = errands.query.filter_by(sno=sno).first()
    db.session.delete(job)
    db.session.commit()
    return redirect('/')



@app.route('/edit/<int:sno>' , methods = ['GET','POST'])
def edit(sno):
    if request.method == 'POST' :
        title = request.form['title']
        desc = request.form['desc']
        pay = request.form['pay']
        job = errands.query.filter_by(sno=sno).first()
        job.job = title
        job.desc = desc
        job.pay = pay

        db.session.add(job)
        db.session.commit()
        return redirect ('/')


    job = errands.query.filter_by(sno=sno).first()
    return render_template('edit.html',job = job)


if __name__== "__main__":
    app.run(debug=True) 