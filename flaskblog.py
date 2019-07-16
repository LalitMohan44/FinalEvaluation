from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file
from forms import RegistrationForm, LoginForm, InterLoginForm, Search, Track
from flask_bcrypt import Bcrypt
import os
import secrets
import pypyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
bcrypt = Bcrypt(app)
conn = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-VQETJ77Q;"
    "Database=ABC;"
    "Trusted_Connection=yes;"
)


@app.route("/")
@app.route("/home")
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    elif 'iloggedin' in session:
        return redirect(url_for('ihome'))
    return redirect(url_for('login'))


@app.route("/ihome", methods=['GET', 'POST'])
def ihome():
    form = Search()
    curs = conn.cursor()
    selec = ("SELECT email, username, contact, skills, noticePeriod, jobID , source "
             "FROM UserProfiles ")
    curs.execute(selec)
    result = curs.fetchall()
    if request.method == 'POST':
        if form.selectN.data == '':
            form.selectN.data = '%'
        select = ("SELECT u.email, username, contact, skills, noticePeriod, jobID , source  "
                  "FROM UserProfiles as u INNER JOIN trackCandidate as t "
                  "ON u.email=t.email "
                  "WHERE skills like ? AND noticePeriod like ? AND jobId like ? AND " + form.selectR.data + " = ?")
        values = [form.selectS.data, form.selectN.data, form.selectJ.data, form.selectT.data]
        print(values)
        curs.execute(select, values)
        result = curs.fetchall()
        if result:
            flash("Filter Applied", 'success')
        else:
            flash("No Record Found", 'danger')
    return render_template('home2.html', form=form, result=result)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}! Login Now', 'success')
        if request.method == 'POST':
            resume_file = save_picture(form.picture.data)
            file = resume_file
            cursor = conn.cursor()
            result = request.form
            insert = ("INSERT INTO UserProfiles "
                      "(email, username, password, contact, noticePeriod, skills, source, jobId) "
                      "VALUES(?,?,?,?,?,?,?,?)")
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            values = list(result.values())
            values = [values[2], values[1].title(), hashed_password, values[5], values[6], values[7], file, values[8]]
            cursor.execute(insert, values)
            conn.commit()
            insert2 = ("INSERT INTO trackCandidate "
                       "(email) "
                       "VALUES(?)")
            cursor.execute(insert2, [form.email.data])
            conn.commit()

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = conn.cursor()
            useremail_form = str(form.email.data)
            select = ("SELECT email,password,username "
                      "FROM UserProfiles "
                      "WHERE email= ?")
            cu.execute(select, [useremail_form])
            results = cu.fetchone()
            password = results[1]
            if useremail_form in results and bcrypt.check_password_hash(password, form.password.data):
                session['loggedin'] = True
                session['id'] = useremail_form
                session['username'] = results[2]
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/ilogin", methods=['GET', 'POST'])
def ilogin():
    form = InterLoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = conn.cursor()
            userid = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT userid,password "
                      "FROM interviewer "
                      "WHERE userid= ?")
            cu.execute(select, [userid])
            results = cu.fetchone()
            if userid and password_form in results:
                session['iloggedin'] = True
                session['iid'] = userid
                flash('You have been logged in!', 'success')
                return redirect(url_for('ihome'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('ilogin.html', title='Login', form=form)


def save_picture(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/profile_pics', file_fn)

    file.save(file_path)

    return file_fn


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        session['photo'] = "default.jpg"
        co = conn.cursor()
        select = ("SELECT email, username, contact, skills, noticePeriod, jobID "
                  "FROM UserProfiles "
                  "WHERE email= ?")
        co.execute(select, [session['id']])
        result = co.fetchone()
        image_file = url_for('static', filename='profile_pics/' + session['photo'])
        return render_template('profile.html', title='Profile', image_file=image_file, result=result)

    return redirect(url_for('login'))


@app.route('/resume/')
def resume():
    cus = conn.cursor()
    select = ("SELECT source "
              "FROM UserProfiles "
              "WHERE email= ?")
    cus.execute(select, [session['id']])
    result = cus.fetchone()
    print(result)
    return send_file("static/profile_pics/"+result[0],
                     attachment_filename=result[0])


@app.route('/download/<resumee>')
def download(resumee):
    return send_file("static/profile_pics/"+resumee,
                     attachment_filename=resumee)


@app.route('/track', methods=['GET', 'POST'])
def track():
    form = Track()
    if form.validate_on_submit():
        candidate = form.selectC.data
        round = form.selectR.data
        status = form.selectS.data
        con = conn.cursor()
        select = ("SELECT email "
                  "FROM UserProfiles "
                  "WHERE username= ?")
        con.execute(select, [candidate])
        result = con.fetchone()
        select = ("SELECT email "
                  "FROM trackCandidate "
                  "WHERE email= ?")
        con.execute(select, [result[0]])
        result2 = con.fetchone()
        print(result2)
        if not result2:
            insert1 = ("INSERT into trackCandidate "
                       "(email) "
                       "VALUES(?)")
            print(str(result[0]))
            con.execute(insert1, [str(result[0])])
            conn.commit()
        insert2 = ("UPDATE trackCandidate "
                   "SET "+round+"= ? "
                   "WHERE email= ?")
        con.execute(insert2, [str(status), str(result[0])])
        conn.commit()
        flash('Success', 'success')
    return render_template('track.html', title='Track', form=form)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/candidate/<email>')
def candidate(email):
    cur = conn.cursor()

    select = ("SELECT email, round1, round2, round3, round4, HR, offers "
              "FROM trackCandidate "
              "WHERE email= ?")
    cur.execute(select, [email])
    result = cur.fetchone()
    return render_template('candidate.html', title='Candidate', result=result)


@app.route('/ilogout')
def ilogout():
    session.pop('iloggedin', None)
    session.pop('iid', None)
    return redirect(url_for('ilogin'))


if __name__ == '__main__':
    app.run(debug=True)
