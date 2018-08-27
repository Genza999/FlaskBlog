from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(20))
    author = db.Column(db.String(20))
    date_time = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/')
def index():
    posts = Blog.query.order_by(Blog.date_time.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blog.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blog(title=title, subtitle=subtitle, author=author,
                content=content, date_time=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
