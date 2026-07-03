from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    uni_id = db.Column(db.String(50), unique=True)
    major = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# الصفحة الأولى (الترحيبية)
@app.route('/')
def index():
    return render_template('index.html')

# الصفحة الثانية (إدخال البيانات + إنشاء البطاقة)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # سحب البيانات من الفورم
        name = request.form['name']
        age = request.form['age']
        uni_id = request.form['uni_id']
        major = request.form['major']

        # حفظ في قاعدة البيانات
        new_student = Student(name=name, age=age, uni_id=uni_id, major=major)
        db.session.add(new_student)
        db.session.commit()

        # عرض صفحة البطاقة وإرسال بيانات الطالب لها
        return render_template('result_card.html', student=new_student)
    
    return render_template('TU_carde_page2.html')

if __name__ == '__main__':
    app.run(debug=True)
    