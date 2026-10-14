from werkzeug.security import generate_password_hash
from conexion import obtener_conexion


usuario = "admin"
contraseña = "123456"

contraseña_hash = generate_password_hash(contraseña)

conexion = obtener_conexion()

if conexion:
    try:
        with conexion.cursor() as cursor:

            sql = "INSERT INTO administrador (usuario, contraseña) VALUES (%s, %s)"
            
            cursor.execute(
                sql,
                (usuario, contraseña_hash)
            )

            conexion.commit()

            print("Administrador creado correctamente")

    except Exception as e:

        print("Error:", e)

    finally:

        conexion.close()