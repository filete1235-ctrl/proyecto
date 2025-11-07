from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

MYSQLHOST = os.environ.get("MYSQLHOST")
MYSQLUSER = os.environ.get("MYSQLUSER")
MYSQLPASSWORD = os.environ.get("MYSQLPASSWORD")
MYSQLDATABASE = os.environ.get("MYSQLDATABASE")
MYSQLPORT = os.environ.get("MYSQLPORT", "3306")  # <- valor por defecto

if not all([MYSQLHOST, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE]):
    raise ValueError("❌ Faltan variables de entorno MySQL en Railway.")

db = mysql.connector.connect(
    host=MYSQLHOST,
    user=MYSQLUSER,
    password=MYSQLPASSWORD,
    database=MYSQLDATABASE,
    port=int(MYSQLPORT)
)


@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT nombre FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template("index.html", usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
    db.commit()
    cursor.close()
    return "Usuario agregado correctamente"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



