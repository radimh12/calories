import datetime
from flask import Flask, render_template
import sqlite3

DATABASE_NAME = "calories.db"

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

@app.route("/")
def calories():
	connection = sqlite3.connect(DATABASE_NAME)
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	cursor.execute("SELECT name, kcal, amount FROM consumed INNER JOIN food ON consumed.food_id = food.id WHERE date = :date", {
		"date": datetime.date.today().isoformat(),
	})

	rows = cursor.fetchall()
	data = []
	total = 0

	for row in rows:
		row = dict(row)

		amount = row["amount"]
		kcal = round(row["kcal"] / 100 * amount)

		data.append({
			"name": row["name"],
			"amount": amount,
			"kcal": kcal,
		})

		total += kcal

	connection.close()
	return render_template("calories.html", data=data, total=total)

@app.route("/food")
def food():
	connection = sqlite3.connect(DATABASE_NAME)
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	cursor.execute("SELECT id, name, kcal FROM food ORDER BY name ASC")

	rows = cursor.fetchall()
	data = []

	for row in rows:
		data.append(dict(row))

	return render_template("food.html", data=data)

def init_db():
	connection = sqlite3.connect(DATABASE_NAME)
	cursor = connection.cursor()

	cursor.execute('''CREATE TABLE IF NOT EXISTS food (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		kcal INTEGER)
	''')

	cursor.execute('''CREATE TABLE IF NOT EXISTS consumed (
		id INTEGER PRIMARY KEY,
		date TEXT NOT NULL,
		food_id INTEGER NOT NULL,
		amount INTEGER)
	''')

	connection.close()

if __name__ == "__main__":
	init_db();
	app.run(debug=True)
