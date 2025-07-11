# app passcode zhac gzde oggy tbf
import sys
print("Running with Python:", sys.executable)
from flask import Flask , render_template , request , redirect , flash , session , url_for , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail , Message
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Errands.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'taskease.project@gmail.com'       
app.config['MAIL_PASSWORD'] = 'kqmageaybnqbvnxg'   
mail = Mail(app)
        

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
s = URLSafeTimedSerializer(app.secret_key)




def send_verification_email(user_email):
    token = s.dumps(user_email, salt='email-confirm')
    link = url_for('confirm_email', token=token, _external=True)
    print(f"Sending verification email to: {user_email}")
    print("Token link:", link)

    msg = ChatMessage("Verify your email", sender="taskease.project@gmail.com", recipients=[user_email])
    msg.body = f"Hi, click this to verify: {link}"
    msg.html = f"<h3>Welcome!</h3><p>Click <a href='{link}'>here</a> to verify.</p>"

    try:
        mail.send(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error while sending email:", e)





class Errands(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    job = db.Column(db.String(200) , nullable = False)
    category = db.Column(db.String(50) )
    desc = db.Column(db.String(500) , nullable = True)
    pay = db.Column(db.Integer , nullable = False)
    date_created = db.Column(db.Date,default=lambda: datetime.now().date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(300), nullable=True)


    def __repr__(self) -> str :
        return f'S.no :  {self.sno} , Title :  {self.job}'
    


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatMessage {self.id}>'





class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    aadhaar = db.Column(db.String(12), nullable=False)
    jobs = db.relationship('Errands', backref='owner', lazy=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    



class AcceptedJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('errands.sno'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    date_accepted = db.Column(db.DateTime, default=datetime.utcnow)

   
    job = db.relationship('Errands', backref=db.backref('accepted_jobs', lazy=True))
    user = db.relationship('User', backref=db.backref('accepted_jobs', lazy=True))




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        aadhaar = request.form.get('aadhaar')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect('/signup')

        # Check if username/email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists", "warning")
            return redirect('/signup')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            address=address,
            aadhaar=aadhaar,
            password=password  # No bcrypt yet, keeping it as plain text for now
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)
        flash("Signup successful! Please check your email to verify your account.", "info")
        return redirect('/login')

    return render_template('signup.html')




@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # 1 hour validity
        user = User.query.filter_by(email=email).first()

        if user:
            user.is_verified = True
            db.session.commit()
            flash("Email verified successfully. You can now log in.", "success")
        else:
            flash("User not found.", "danger")
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
    
    return redirect('/login')



@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST' :

        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter((User.email == email) | (User.username == email)).first()

        ''' if existing_user:
            if not existing_user.is_verified:
                flash("Please verify your email before logging in.", "warning")
                return redirect('/login')

        if existing_user and existing_user.password == password:  
            session['user_id'] = existing_user.id  
            session["username"] = existing_user.username
            flash("Login successful!", "success")
            return redirect('/dashboard')  
        flash("Invalid credentials. Please try again.", "danger") '''

        # below code if for demo
        if email == 'demo@taskease.com' and password == '1234':
            session['user_id'] = 1  # Arbitrary ID
            session["username"] = "DemoUser"
            flash("Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("Invalid credentials. Try demo@taskease.com / 1234", "danger")


    return render_template('login.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect('/login')

    username = session.get('username')
    search_query = request.args.get('search', '')
    selected_category = request.args.get('category', 'All')

    alljobs = Errands.query

    # Filter by search
    if search_query:
        keywords = [word.strip() for word in search_query.split(',')]
        search_filter = or_(
            *[Errands.desc.ilike(f"%{word}%") | Errands.job.ilike(f"%{word}%") for word in keywords]
        )
        alljobs = alljobs.filter(search_filter)

    # Filter by category
    if selected_category != 'All':
        alljobs = alljobs.filter_by(category=selected_category)

    alljobs = alljobs.order_by(Errands.sno.desc()).all()

    return render_template('dashboard.html', user=user, username=username, alljobs=alljobs, selected_category=selected_category, search_query=search_query)



@app.route("/",methods=['GET'])
def TaskEase():
    session.pop('user_id', None)  
    session.pop('username', None)
    
    alljobs = Errands.query.all()

    logged_in = 'user_id' in session

    return render_template("index.html" , alljobs = alljobs , logged_in=logged_in)


@app.route("/p_id")
def p_id():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    return render_template('p_id.html',user=user)


@app.route('/remove/<int:sno>')
def remove(sno):
    if 'user_id' not in session:
        flash("Please log in to delete jobs.", "danger")
        return redirect('/login')

    job = Errands.query.filter_by(sno=sno, user_id=session['user_id']).first()
    if not job:
        return redirect('/dashboard')

    db.session.delete(job)
    db.session.commit()
    return redirect('/dashboard')




@app.route('/chat/<int:receiver_id>', methods=['GET', 'POST'])
def chat(receiver_id):
    if 'user_id' not in session:
        return redirect('/login')

    sender_id = session['user_id']
    receiver = User.query.get(receiver_id)

    if not receiver:
        flash("User not found.", "danger")
        return redirect('/dashboard')

    job_id = request.args.get('job_id', type=int)
    print("Job ID:", job_id)

    job = None
    if job_id:
        job = Errands.query.filter_by(sno=job_id).first()  # Changed from `get` to `filter_by`

    # Handle sending a message (POST)
    if request.method == 'POST':
        if request.is_json:
            content = request.json.get('message')
            if content:
                new_msg = ChatMessage(sender_id=sender_id, receiver_id=receiver_id, content=content)
                db.session.add(new_msg)
                db.session.commit()
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "error": "Message content missing"}), 400

    # Get chat history between the two users (GET)
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == sender_id) & (ChatMessage.receiver_id == receiver_id)) |
        ((ChatMessage.sender_id == receiver_id) & (ChatMessage.receiver_id == sender_id))
    ).order_by(ChatMessage.timestamp.desc()).all()

    # Reverse the message order to show the latest at the bottom
    messages.reverse()

    current_user = User.query.get(sender_id)

        
    return render_template('chat.html', receiver=receiver, messages=messages, job=job ,current_user=current_user)





@app.route('/chat/<int:receiver_id>', methods=['POST'])
def send_message(receiver_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json()
    content = data.get('message')
    sender_id = session['user_id']

    if not content:
        return jsonify({"success": False, "error": "Empty message"}), 400

    # Save to database
    new_msg = ChatMessage(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": {
            "id": new_msg.id,
            "sender_id": new_msg.sender_id,
            "receiver_id": new_msg.receiver_id,
            "content": new_msg.content,
            "timestamp": new_msg.timestamp.isoformat()
        }
    }), 200





@app.route('/chat/<int:receiver_id>/messages', methods=['GET'])
def get_messages(receiver_id):
    if 'user_id' not in session:
        return redirect('/login')

    sender_id = session['user_id']

    # Fetch all messages between sender and receiver
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == sender_id) & (ChatMessage.receiver_id == receiver_id)) |
        ((ChatMessage.sender_id == receiver_id) & (ChatMessage.receiver_id == sender_id))
    ).order_by(ChatMessage.timestamp.asc()).all()

    # Return messages in the required format
    message_data = [{"id": msg.id, "content": msg.content, "sender_id": msg.sender_id} for msg in messages]

    return jsonify({
        "messages": message_data,
        "newMessages": len(message_data) > 0  # Indicate if there are new messages
    })





@app.route("/contacts")
def contacts():
    if 'user_id' not in session:  
        flash("Please log in to see available tasks.", "danger")
        return redirect('/login')
    return render_template("contacts.html")



@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/tasks")
def tasks():
    if 'user_id' not in session:  
        flash("Please log in to see available tasks.", "danger")
        return redirect('/login')
    alljobs = Errands.query.filter(Errands.user_id != session['user_id']).all()   
    return render_template('tasks.html',alljobs = alljobs)




@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect("/")



@app.route('/edit/<int:sno>' , methods = ['GET','POST'])
def edit(sno):
    if request.method == 'POST' :
        title = request.form['title']
        desc = request.form['desc']
        pay = request.form['pay']

        if 'user_id' not in session:
            flash("Please log in to edit jobs.", "danger")
            return redirect('/login')

        job = Errands.query.filter_by(sno=sno, user_id=session['user_id']).first()
        if not job:
            flash("Unauthorized action.", "danger")
            return redirect('/dashboard')
        
        job = Errands.query.filter_by(sno=sno).first()
        job.job = title
        job.desc = desc
        job.pay = pay

        db.session.add(job)
        db.session.commit()
        return redirect ('/')

    job = Errands.query.filter_by(sno=sno).first()
    return render_template('edit.html',job = job)



@app.route('/testmail')
def testmail():
    msg = Message("Test Email", sender="taskease.project@gmail.com", recipients=["hariom2045khete@gmail.com"])
    msg.body = "If you're seeing this, Flask-Mail is working!"
    mail.send(msg)
    return "Mail sent!"



@app.route('/resend_verification', methods=['POST'])
def resend_verification():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        if user.is_verified:
            flash("Email is already verified. You can log in.", "info")
        else:
            send_verification_email(email)
            flash("Verification email resent. Check your inbox.", "info")
    else:
        flash("No account associated with this email.", "warning")
    
    return redirect('/login')



@app.route("/postjob", methods=["GET", "POST"])
def postjob():
    if 'user_id' not in session:
        flash("Please log in to post a job.", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session['user_id'])

    if request.method == "POST":
        job = request.form.get("job")
        category = request.form.get("category")
        desc = request.form.get("desc")
        pay = request.form.get("pay")
        location = request.form.get("location")
        skills = request.form.get("skills")

        if not (job and category and pay and location):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for("postjob"))

        new_job = Errands(

            job=job,
            category=category,
            desc=desc,
            pay=int(pay),
            user_id=user.id,
            location=location,
            skills=skills,
        )

        db.session.add(new_job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for("dashboard"))
   
    return render_template("postjob.html", user=user)
    



if __name__== "__main__":
    app.run(debug=True) 