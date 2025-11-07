from urllib.parse import urlparse
import os
import mysql.connector

# Obtener la URL de conexión de Railway
url_str = os.environ.get("DATABASE_URL")

if not url_str:
    raise ValueError("❌ No se encontró la variable DATABASE_URL en Railway")

# Parsear la URL
url = urlparse(url_str)

# Definir puerto por defecto si no existe
port = url.port or 3306

# Conexión a MySQL
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path.lstrip("/"),  # elimina la barra inicial
    port=port
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


