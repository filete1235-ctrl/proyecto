from flask import Flask, render_template, request
import mysql.connector
import os

from urllib.parse import urlparse
import os
import mysql.connector

app = Flask(__name__)
url = urlparse(os.environ.get("DATABASE_URL"))

db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],
    port=url.port or 3306
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

