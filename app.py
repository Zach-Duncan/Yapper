from flask import Flask, render_template, request, redirect, session, url_for
from db import DBConnection  # You’ll create this in db.py
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = DBConnection.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get subscribed topics
    cursor.execute("""
        SELECT t.id, t.title 
        FROM topics t
        JOIN subscriptions s ON t.id = s.topic_id
        WHERE s.user_id = %s
    """, (session['user_id'],))
    topics = cursor.fetchall()

    # For each topic, get last 2 messages
    messages_by_topic = {}
    for topic in topics:
        cursor.execute("""
            SELECT m.content, m.created_at, u.username 
            FROM messages m
            JOIN users u ON u.id = m.user_id
            WHERE m.topic_id = %s
            ORDER BY m.created_at DESC
            LIMIT 2
        """, (topic['id'],))
        messages_by_topic[topic['title']] = cursor.fetchall()

    return render_template('home.html', messages_by_topic=messages_by_topic)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # You should hash this in production

        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return "Invalid login"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/topics')
def topics():
    conn = DBConnection.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all topics
    cursor.execute("SELECT * FROM topics")
    topics = cursor.fetchall()

    return render_template('topics.html', topics=topics)


@app.route('/subscribe/<int:topic_id>')
def subscribe(topic_id):
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO subscriptions (user_id, topic_id) VALUES (%s, %s)", (session['user_id'], topic_id))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/unsubscribe/<int:topic_id>')
def unsubscribe(topic_id):
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE user_id = %s AND topic_id = %s", (session['user_id'], topic_id))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/post/<int:topic_id>', methods=['POST'])
def post_message(topic_id):
    content = request.form['content']
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (topic_id, user_id, content) VALUES (%s, %s, %s)", (topic_id, session['user_id'], content))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/stats')
def stats():
    conn = DBConnection.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, access_count FROM topics")
    stats = cursor.fetchall()
    return render_template('stats.html', stats=stats)

# --------------- END ROUTES ----------------

if __name__ == '__main__':
    app.run()
