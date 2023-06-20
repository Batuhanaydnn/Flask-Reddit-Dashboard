from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import praw

app = Flask(__name__)
app.app_context().push()
app.secret_key = 'supersecretkey'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.name

# Define Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    upvotes = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    video_link = db.Column(db.String(200))
    image_link = db.Column(db.String(200))

    def __repr__(self):
        return '<Post %r>' % self.title

# Define routes for login and registration
@app.route('/')
def home():
    return render_template('home.html')

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
    return render_template('register.html')

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()

        if request.method == 'POST':
            
            filter_text = request.form['filter_text']  

            # Connect to Reddit API
            reddit = praw.Reddit(client_id='JMqEtE1wdrD39jhY_ZwTQA',
                                 client_secret='dDqqLlBcblEFzj9EylLgckbPIHdz6w',
                                 user_agent='technicalqualifierwasveryeasy')
            subreddit = reddit.subreddit('popular')

            # Crawl new posts and add them to database
            for post in subreddit.new(limit=100):
                # Check if post already exists in database and matches the filter
                if not db.session.query(Post).filter(Post.title == post.title, Post.title.contains(filter_text)).first():
                    # Create a dictionary to store post information
                    post_data = {
                        'title': post.title,
                        'content': post.selftext,
                        'upvotes': post.score,
                        'comment_count': post.num_comments,
                        'video_link': None,
                        'image_link': None
                    }

                    # Check if the post is a video post
                    if post.is_video:
                        post_data['video_link'] = post.media['reddit_video']['fallback_url']
                    # Check if the post is an image post
                    elif post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        post_data['image_link'] = post.url

                    # Create new post and add to database
                    new_post = Post(user=user, **post_data)
                    db.session.add(new_post)
                    db.session.commit()

            # Get filtered posts from database
            posts = Post.query.filter(Post.title.contains(filter_text)).all()

            if request.headers.get('accept') == 'application/json':
                # If the request accepts JSON, return the filtered posts as JSON
                json_posts = []
                for post in posts:
                    json_post = {
                        'title': post.title,
                        'content': post.content,
                        'upvotes': post.upvotes,
                        'comment_count': post.comment_count,
                        'video_link': post.video_link,
                        'image_link': post.image_link
                    }
                    json_posts.append(json_post)
                return jsonify(posts=json_posts)
            else:
                # Otherwise, render the dashboard template with filtered posts
                return render_template('dashboard.html', user=user, posts=posts, filter_text=filter_text)

        else:
            # Get all posts from database
            posts = Post.query.all()

            # Render the dashboard template with all posts
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
    db.create_all()
    app.run(debug=True)
