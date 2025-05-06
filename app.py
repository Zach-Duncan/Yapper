import os
from flask import Flask, render_template, request, redirect, session, url_for
from db import DBConnection
from Models.user import User
from Models.topic import Topic
from Models.message import Message
from observer import TopicAccessObserver

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
observer = TopicAccessObserver()

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    topics = Topic.get_subscribed(session['user_id'])
    messages = {t['id']: Message.get_recent_by_topic(t['id']) for t in topics}
    return render_template('home.html', topics=topics, messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.login(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        User.register(request.form['username'], request.form['password'])
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/topics')
def topics():
    all_topics = Topic.get_all()
    for topic in all_topics:
        observer.notify(topic['id'])
    return render_template('topics.html', all_topics=all_topics)

@app.route('/topic/<int:topic_id>')
def topic_view(topic_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    topic = Topic.get_by_id(topic_id)
    if not topic:
        return "Topic not found", 404
    
    Topic.increment_access_count(topic_id)
    is_subscribed = Topic.is_user_subscribed(session['user_id'], topic_id)
    members = Topic.get_subscribers(topic_id)
    messages = Message.get_all_by_topic(topic_id)

    # Debugging: Check the user_id and topic.user_id
    print(f"Session User ID: {session['user_id']}")
    print(f"Topic User ID: {topic.user_id}")

    return render_template('topic_view.html', topic=topic, is_subscribed=is_subscribed, members=members, messages=messages, user_id=session['user_id'])


@app.route('/create-topic', methods=['GET', 'POST'])
def create_topic():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = session['user_id']
        if title and description and user_id:
            Topic.create(title, user_id, description)
            return redirect(url_for('topics'))
    return render_template('create_topic.html')

@app.route('/delete-topic/<int:topic_id>', methods=['POST'])
def delete_topic(topic_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    topic = Topic.get_by_id(topic_id)
    if not topic or topic['user_id'] != session['user_id']:
        return "Unauthorized", 403

    Topic.delete_topic(topic_id)
    return redirect(url_for('topics'))


@app.route('/subscribe/<int:topic_id>')
def subscribe(topic_id):
    db = DBConnection.get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT IGNORE INTO subscriptions (user_id, topic_id) VALUES (%s, %s)", (session['user_id'], topic_id))
    db.commit()
    return redirect(url_for('topic_view', topic_id=topic_id))

@app.route('/unsubscribe/<int:topic_id>')
def unsubscribe(topic_id):
    db = DBConnection.get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE user_id = %s AND topic_id = %s", (session['user_id'], topic_id))
    db.commit()
    return redirect(url_for('topic_view', topic_id=topic_id))

@app.route('/post', methods=['POST'])
def post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    topic_id = request.form['topic_id']
    content = request.form['content']
    if content:
        Message.post_message(user_id, topic_id, content)
    return redirect(url_for('topic_view', topic_id=topic_id))

@app.route('/delete-message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    message = Message.get_by_id(message_id)
    if message and message['user_id'] == user_id:
        Message.delete_message(message_id)
    return redirect(url_for('topic_view', topic_id=message['topic_id']))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "10000")) 
    app.run(host="0.0.0.0", port=port)

