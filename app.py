from flask import Flask, render_template, request, flash, session, redirect, send_file, get_flashed_messages
import sqlite3
import os
from image import get_image_url
from find_out import find_out
from currency import currency_converter
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from translate import check_language,from_ka_to_en



app = Flask(__name__)
app.config['SECRET_KEY'] = 'JGSABGJBSGJBSDAUIGHSIUGHASIUGHSDHAGUH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique = False, nullable=False)
    username = db.Column(db.String(50), unique = True, nullable=False)
    email = db.Column(db.String(50), unique = True, nullable=False)
    password = db.Column(db.String(200), unique = True, nullable=False)



@app.route('/')
def home():

    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    data = c.execute('SELECT * FROM weather').fetchall()
    conn.close()
    return render_template('home.html', data=data)


@app.route('/aboutus')
def aboutus():
    return render_template('about_us.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    if check_language(query) == 'ka':
        query = from_ka_to_en(query)

    try:
        response = find_out(query)
        image_url = get_image_url(query)

    except Exception:
        flash("გთხოვთ შეიყვანეთ შესაბამის ქალაქის/სოფლის დასახელება!",'error')
        return render_template('search.html')

    return render_template('search.html', title=query, forecast=response, image_url=image_url)


@app.route('/news')
def news():

    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    data = cursor.execute('SELECT * FROM news').fetchall()
    conn.close()
    return render_template('news.html', data=data)

@app.route('/news/read_more', methods=['GET', 'POST'])

def read_more(title=None,content=None,image=None):
    title = request.args.get('title')
    content = request.args.get('content')
    image = request.args.get('image')
    time = request.args.get('time')
    return render_template('read_more.html', title=title,
                           content=content, image=image, time=time)


@app.route('/currency')
def currency():

    conn = sqlite3.connect('currency.db')
    cursor = conn.cursor()
    data = cursor.execute('SELECT * FROM VALUTA').fetchall()
    conn.close()
    return render_template('currency.html', data=data)
@app.route('/currency/convert', methods=['GET', 'POST'])
def convert(fromm=None, to=None, amount=None):

    fromm = request.args.get('from-currency')
    to = request.args.get('to-currency')
    amount = request.args.get('amount')
    result = currency_converter(fromm, to, amount)
    return render_template('convert_currency.html',result = result, fromm = fromm,
to = to, amount =amount)


@app.route('/currency/download')
def download():

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'currency.json')
    return send_file(file_path, as_attachment=True)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        with app.app_context():
            try:
                db.create_all()
                user = User(name=name,lastname=lastname,username=username,email=email,password=password)
                db.session.add(user)
                db.session.commit()
                flash('თქვენი აქაუნთი წარმატებით შეიქმნა!', 'success')

            except Exception:
                flash('ეს username/პაროლი უკვე გამოყენებულია','error')

    return render_template('sign_up.html')


@app.route('/login',methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter((User.username == username)).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect('/')
        else:
            flash('შეყვანილი username/პაროლი არასწორია!', 'error')
            return render_template('login.html')


    return render_template('login.html')


@app.route('/logout',methods=['POST','GET'])
def log_out():

    session.pop('username', None)
    return redirect('/')


@app.route('/mypage')
def my_page():

    info = User.query.filter((User.username == session['username'])).first()
    return render_template('my_page.html',info=info)


if __name__ == '__main__':
    app.run(debug=True)
