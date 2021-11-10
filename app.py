from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(database="service",
                        user="postgres",
                        password="123",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/', methods=['POST','GET'])
def index():
    return redirect("/login/")

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if (not username) or (not password):
                return render_template('error.html')

            try:

                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = cursor.fetchone()[0]
            except TypeError:
                return render_template("er.html")
            return render_template('account.html', full_name=records)

        elif request.form.get("registration"):
            return redirect("/registration/")


    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if (not name) or (not login) or (not password):
            return render_template("error.html")
        if not name.isalpha():
            return render_template("number.html")
        if login:
            cursor.execute('SELECT * FROM service.users')
            rows = cursor.fetchall()
            for row in rows:
                if login == row[2]:
                    return render_template("repeat.html")
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()

        return redirect('/login/')
    return render_template('registration.html')

