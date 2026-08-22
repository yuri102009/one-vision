import pymysql


def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host="localhost",
            database="one_vision",
            user="root",
            password="root",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Conexión exitosa a la base de datos")
        return conexion

    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
