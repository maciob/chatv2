from locale import format_string
from logging import root
from flask import Flask,render_template, request
import psycopg2
from datetime import datetime

app = Flask(__name__)


conn = psycopg2.connect(database="mydb",
                        host="postgres",
                        user="app",
                        password="pass",
                        port="5432")


@app.route("/<int:room_id>",methods=["GET","POST"])
def home(room_id):
	return render_template("index.html")

@app.route("/api/chat/<int:room_id>",methods=["GET","POST"])
def send(room_id):
	conn = psycopg2.connect(database="mydb", host="postgres", user="app", password="pass", port="5432")
	cur = conn.cursor()
	cur.execute(f"CREATE TABLE IF NOT EXISTS chat ( ID INT , username VARCHAR (30) , message VARCHAR (250) , data VARCHAR (50) );")
	row = ""
	if request.method == "GET":
		cur.execute(f"SELECT * FROM chat WHERE ID in ('{room_id}')")
		data = cur.fetchall()
		response = []
		if data:
			for i in data:
				response.append(f'({i[3]} {i[1]}): {i[2]}')
			return "\n".join(response)
		else:
			return "EMPTY HISTORY"
	if request.method == "POST":
		message = request.form.get("msg")
		username = request.form.get("username")
		date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		cur.execute(f"INSERT INTO chat (ID,username,message,data) VALUES ('{room_id}','{username}','{message}','{date}');")
		conn.commit()
		return f'{message}'
if __name__ == "__main__":
	app.run()
