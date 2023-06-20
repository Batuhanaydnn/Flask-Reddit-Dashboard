from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import praw
from models import db, User, Post

app = Flask(__name__)
app.app_context().push()

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid email or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()

        # Connect to Reddit API
        reddit = praw.Reddit(client_id='JMqEtE1wdrD39jhY_ZwTQA',
                             client_secret='dDqqLlBcblEFzj9EylLgckbPIHdz6w',
                             user_agent='technicalqualifierwasveryeasy')
        subreddit = reddit.subreddit('netsec')

        for post in subreddit.new(limit=10):
            if not db.session.query(Post).filter(Post.title == post.title).first():
                new_post = Post(title=post.title, content=post.selftext, user=user)
                db.session.add(new_post)
                db.session.commit()

        posts = Post.query.all()

        if request.headers.get('accept') == 'application/json':
            return jsonify(posts=[post.__dict__ for post in posts])
        else:
            return render_template('dashboard.html', user=user, posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/api/posts/')
def api_posts():
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        post_dict = {}
        for key, value in post.__dict__.items():
            if key != '_sa_instance_state':
                post_dict[key] = value
        posts_list.append(post_dict)
    return jsonify(posts=posts_list)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)