from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from deepfake_detector import detect_deepfake  # Importing the detection function
#python -m --app flask .\app.py run
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models (User, DetectionResult, Report)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    detections = db.relationship('DetectionResult', backref='user', lazy=True)

class DetectionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed! Check your credentials and try again.', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            # Call the deepfake detection function
            result = detect_deepfake(file_path)
            
            detection = DetectionResult(user_id=session['user_id'], file_path=file_path, result=result)
            db.session.add(detection)
            db.session.commit()

            return f'Detection result: {result}'

    return render_template('dashboard.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        description = request.form['description']
        contact_info = request.form['contact']
        file = request.files['file']
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('reports', filename)
            file.save(file_path)
        
        report = Report(description=description, contact_info=contact_info, file_path=file_path)
        db.session.add(report)
        db.session.commit()
        
        flash('Your report has been submitted successfully. We will contact you soon.', 'success')
        return redirect(url_for('report'))
    
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
