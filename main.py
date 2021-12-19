from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    age = request.args.get('age')
    user = User(
        age=age,
        gender=gender
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5)
    db.session.add(answer)
    db.session.commit()
    db.session.refresh(answer)
    return render_template('process.html')

@app.route('/statistics')
def statistics_page():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    q1_answers = db.session.query(Answers.q1).all()
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0]
    q2_answers = db.session.query(Answers.q2).all()
    all_info['q3_mean'] = db.session.query(func.avg(Answers.q3)).one()[0]
    q3_answers = db.session.query(Answers.q3).all()
    all_info['q4_mean'] = db.session.query(func.avg(Answers.q4)).one()[0]
    q4_answers = db.session.query(Answers.q4).all()
    all_info['q5_mean'] = db.session.query(func.avg(Answers.q5)).one()[0]
    q5_answers = db.session.query(Answers.q5).all()
    return render_template('statistics.html', all_info=all_info)

# @app.route('/statistics')
# def statistics_page():
#     return render_template('statistics.html')

if __name__ == '__main__':
    app.run()