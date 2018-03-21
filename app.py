from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from data import articles_dstore
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
# from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)

# config mysql
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ESTD1759'
app.config['MYSQL_DATABASE_DB'] = 'myflask'
app.config['MYSQL_DATABASE_CURSORCLASS'] = 'Dictcursor'

# init mysql

mysql = MySQL(app)


article = articles_dstore()


@app.route('/index')
@app.route('/index/<path:name>')
def index(name=None):
    """Complete this docstring"""
    return render_template('dynamic.html', name=name)


@app.route('/articles')
def articles():
    """Complete this docstring"""
    return render_template('articles.html', article=article)


@app.route('/article/<string:article_id>')
def article(article_id):
    """Complete this docstring"""
    return render_template('article.html', article_id=article_id)


class RegisterForm(Form):
    username = StringField('Name', [validators.Length(min=1, max=10)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo(
                                          'confirm',
                                          message='Passwords do not match')
                                          ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.get_db().cursor()
        # execute query
        cur.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.get_db().commit()
        # close cursor
        cur.close()

        flash('Bravo,  You are a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
