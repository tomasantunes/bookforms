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

	sql_books_table = """ CREATE TABLE IF NOT EXISTS books (
							id integer PRIMARY KEY,
							title text,
							description text,
							author integer,
							creation_date date
						); """

	c.execute(sql_books_table)

@app.route("/")
def books():
	db = connect_db()
	c = db.execute('SELECT * FROM books')
	rows = c.fetchall()
	books = []

	for row in rows:
		book = {
			'title': row[1],
			'description' : Markup(row[2]),
			'author' : row[3],
			'creation_date' : datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
			'chapters' : [],
		}

		db = connect_db()
		c = db.execute('SELECT * FROM books INNER JOIN chapters on books.id = chapters.book_id;')
		comments = c.fetchall()

		for c in chapters:
			book.chapters.append(c)

		books.append(book)

	return render_template("books.html", books=books)

@app.route("/book-info/<book>")
def home(book):
	return render_template("book-info.html", book=book)
		
@app.route("/add-book", methods=['POST'])
def add_book():
	title = request.form.get('title', "")
	author = request.form.get('author', "")
	description = request.form.get('description', "")

	date = datetime.datetime.now()

	if (title != "" and content != ""):
		db = connect_db()
		db.execute('INSERT INTO books (title, author, description, date) VALUES (?, ?, ?, ?)', [title, author, description, date])
		db.commit()
		return redirect("/books")
	return redirect("/books")
 
if __name__ == "__main__":
	init()
	app.run()