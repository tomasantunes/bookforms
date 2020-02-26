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
							author text,
							date date
						); """

	c.execute(sql_books_table)

	sql_chapters_table = """ CREATE TABLE IF NOT EXISTS chapters (
							id integer PRIMARY KEY,
							book_id integer,
							title text,
							chapter text,
							date date
						); """

	c.execute(sql_chapters_table)

def getBooksList():
	db = connect_db()
	c = db.execute('SELECT * FROM books')
	rows = c.fetchall()
	books = []

	for row in rows:
		book = {
			'id': row[0],
			'title': row[1],
			'description' : Markup(row[2]),
			'author' : row[3],
			'date' : datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
			'chapters' : [],
		}

		db = connect_db()
		c = db.execute('SELECT * FROM chapters INNER JOIN books on books.id = chapters.book_id WHERE books.id = ?;', [book['id']])
		chapters = c.fetchall()

		for c in chapters:
			chapter = {
				'id': c[0],
				'book_id': c[1],
				'title' : c[2],
				'chapter' : Markup(c[3]),
				'date' : datetime.datetime.strptime(c[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
			}
			book['chapters'].append(chapter)

		books.append(book)
	
	return books

def getBookById(id):
	db = connect_db()
	c = db.execute('SELECT * FROM books WHERE id = ?', [id])
	rows = c.fetchall()
	b = rows[0]
	
	print(id)
	print(b)

	book = {
		'id':b[0],
		'title': b[1],
		'description' : Markup(b[2]),
		'author' : b[3],
		'date' : datetime.datetime.strptime(b[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
		'chapters' : [],
	}

	db = connect_db()
	c = db.execute('SELECT * FROM chapters INNER JOIN books on books.id = chapters.book_id WHERE books.id = ?;', [id])
	chapters = c.fetchall()

	for c in chapters:
		chapter = {
			'id': c[0],
			'book_id': c[1],
			'title' : c[2],
			'chapter' : Markup(c[3]),
			'date' : datetime.datetime.strptime(c[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
		}
		book['chapters'].append(chapter)

	return book

@app.route("/")
def books():
	books = getBooksList()
	return render_template("books.html", books=books)

@app.route("/book-info")
def bookInfoNew():
	return render_template("book-info.html")

@app.route("/book-info/<book>")
def bookInfoById(book):
	books = getBooksList()
	return render_template("book-info.html", book=book, books=books)

@app.route("/get-book/")
def getBookByIdRoute():
	id = request.args.get('id', "")
	book = getBookById(id)
	return jsonify(book)

@app.route("/edit-chapter/<book>")
def editChapter(book):
	return render_template("edit-chapter.html", book=book)

@app.route("/edit-chapter/<book>/<chapter>")
def editChapterById(book, chapter):
	return render_template("edit-chapter.html", book=book, chapter=chapter)
		
@app.route("/save-book-info", methods=['POST'])
def add_book():
	title = request.form.get('title', "")
	author = request.form.get('author', "")
	description = request.form.get('description', "")

	date = datetime.datetime.now()

	if (title != "" and author != "" and description != ""):
		db = connect_db()
		db.execute('INSERT INTO books (title, author, description, date) VALUES (?, ?, ?, ?)', [title, author, description, date])
		db.commit()
		return redirect("/")
	return redirect("/")

@app.route("/save-chapter/<book>", methods=['POST'])
def saveChapter(book):
	book_id = book
	title = request.form.get('title', "")
	chapter = request.form.get('chapter', "")

	date = datetime.datetime.now()

	if (book_id != "" and title != "" and chapter != ""):
		db = connect_db()
		db.execute('INSERT INTO chapters (book_id, title, chapter, date) VALUES (?, ?, ?, ?)', [book_id, title, chapter, date])
		db.commit()
		return redirect("/")
	return redirect("/")
 
if __name__ == "__main__":
	init()
	app.run()