from flask import Flask, render_template

app = Flask(__name__, template_folder="html")

@app.get("/")
def home():
	return "Welcome to the docs template!"

@app.get("/lexical_analysis")
def lexical_analysis():
	return render_template("lexer.html")

@app.errorhandler(404)
def notfound():
	return "Oops! The requested URL was not found!"