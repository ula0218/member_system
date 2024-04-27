1.引入必要的Python庫和模組，包括 Flask、render_template、request、redirect、flash等，也引入了 MySQL Connector 來連接和操作 MySQL 資料庫
```
from flask import Flask, render_template, request,url_for,redirect,flash
from wtforms import StringField, PasswordField, SubmitField
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, InputRequired,ValidationError,Length 
import mysql.connector
```
2.生成虛擬環境
```
$ python -m venv venv
$ source venv/bin/activate
$ deactivate
```
