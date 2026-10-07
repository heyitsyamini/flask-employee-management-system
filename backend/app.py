
from flask import Flask, jsonify, send_from_directory, request
import mysql.connector

app = Flask(__name__)


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxxxxx",
        database="interview_db"
    )

    return connection


@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/style.css")
def style():
    return send_from_directory("../frontend", "style.css")

@app.route("/script.js")
def script():
    return send_from_directory("../frontend", "script.js")

@app.route("/employees", methods=["GET"])
def get_employees():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True) #the thing Python uses to send SQL to MySQL.
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall() #This takes all the rows MySQL returned.
    cursor.close()
    connection.close()
    return jsonify(employees)

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    department = data["department"]
    salary = data["salary"]
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO employees (name, email, department, salary)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, email, department, salary))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Employee added successfully"})

@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    department = data["department"]
    salary = data["salary"]

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE employees
        SET name = %s,
            email = %s,
            department = %s,
            salary = %s
        WHERE id = %s
    """

    cursor.execute(query, (name, email, department, salary, id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Employee updated successfully"})

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        DELETE FROM employees
        WHERE id = %s
    """
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)