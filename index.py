from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__);
app.secret_key = "flash message";

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="students"
)

@app.route('/')
def index():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM information");
	data = mycursor.fetchall()
	return render_template('index.html', students=data);


@app.route('/insert', methods=['POST'])
def insert():
	flash("Data inserted successfully");
	if request.method == "POST":
		name = request.form['name'];
		email = request.form['email'];
		phone = request.form['phone'];

		mycursor = mydb.cursor()
		sql = "INSERT INTO information (name, email, phone) VALUES (%s, %s, %s)"
		val = (name, email, phone)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('index'));

@app.route('/update', methods=['POST'])	
def update():
	if request.method == 'POST':
		id_data = request.form['id'];
		name = request.form['name'];
		email = request.form['email'];
		phone = request.form['phone'];

		mycursor = mydb.cursor()
		mycursor.execute("""
			UPDATE information
			SET name=%s, email=%s, phone=%s
			WHERE id=%s
			""", (name, email, phone, id_data));
		mydb.commit()
		flash("Data Updated Successfully");
		return redirect(url_for('index'));

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM information WHERE id=%s", (id_data,))
    mydb.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True);