from flask import Flask, render_template, request, flash, jsonify, session, redirect, Markup
import sqlite3
import datetime
import os

def connect_db():
	return sqlite3.connect("bookforms.db")

db = connect_db()

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "default_key"

def init():
	db = connect_db()
	c = db.cursor()

	sql_posts_table = """ CREATE TABLE IF NOT EXISTS posts (
							id integer PRIMARY KEY,
							title text,
							content text,
							author integer,
							date date
						); """

	c.execute(sql_posts_table)

@app.route("/")
def home():
	db = connect_db()
	c = db.execute('SELECT * FROM posts')
	rows = c.fetchall()
	posts = []

	for row in rows:
		post = {
			'title': row[1],
			'content' : Markup(row[2]),
			'author' : row[3],
			'date' : datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
			'comments' : [],
		}

		db = connect_db()
		c = db.execute('SELECT * FROM comments INNER JOIN posts on posts.id = comments.post_id;')
		comments = c.fetchall()

		for c in comments:
			post.comments.append(c)

		posts.append(post)

	return render_template("home.html", posts=posts)
		
@app.route("/add-post", methods=['POST'])
def add_post():
	user_id = session['user_id']
	title = request.form.get('title', "")
	content = request.form.get('content', "")

	date = datetime.datetime.now()

	if (title != "" and content != ""):
		db = connect_db()
		db.execute('INSERT INTO posts (title, content, author, date) VALUES (?, ?, ?, ?)', [title, content, user_id, date])
		db.commit()
		return redirect("/home")
	return redirect("/home")
 
if __name__ == "__main__":
	init()
	app.run()