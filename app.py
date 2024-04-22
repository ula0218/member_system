from flask import Flask, render_template, request,url_for,redirect,flash
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, SubmitField
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, InputRequired,ValidationError,Length 
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydatabase'

class User(FlaskForm):
    username = StringField(label='用戶名', validators=[InputRequired('用戶名不得為空'),Length(min=4,max=20)])
    password = PasswordField(label='密碼', validators=[InputRequired('密碼不得為空'),Length(min=4,max=20)])
    password_twice = PasswordField(label='再次輸入密碼', validators=[DataRequired('密碼不得為空'), EqualTo('password', message='兩次密碼輸入不一致')])
    submit = SubmitField(label='提交')    
    
    def validators_username(self,username):
        existing_user_name= user.query.filter_by(
            username = username.data).first()
        
        if existing_user_name:
            raise ValidationError('使用者名稱已使用')

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'tina00012',
    'database': 'member',
    'autocommit': True
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='log_in'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register',methods=['GET','POST'])
def register():
    form = User()
    if request.method == 'GET':
        return render_template('register.html',form = form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password_twice = form.password_twice.data
            print(username, password)

            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            create_table_query = """
                CREATE TABLE IF NOT EXISTS user (
                    id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255),
                    password VARCHAR(255),
                    UNIQUE KEY (name, password)
            )
            """
            cursor.execute(create_table_query)
            insert_data_query = "INSERT INTO user (name, password) VALUES (%s, %s)"
            data = (username, password)
            cursor.execute(insert_data_query, data)

            db.commit()
        else:
            return '驗證失敗'
        flash('註冊成功', 'success')
        return redirect(url_for('log_in')) 


@app.route('/log_in',methods=['GET','POST'])
def log_in():
    form = User()
    if request.method == 'GET':
        return render_template('login.html',form = form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        query = "SELECT * FROM user WHERE name = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user:
            if password == user[2]:
                flash('登入成功', 'success')
                return redirect(url_for('welcome', username=username)) 
            else:
                flash('密碼錯誤', 'error')
        else:
            flash('用戶不存在', 'error')
            return redirect(url_for('register')) 
    return render_template('login.html', form=form)

@app.route('/')    
def home():
    return render_template('home.html')

@app.route('/welcome/<username>')    
def welcome(username):
    return render_template('welcome.html',  username=username)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port = 3300)