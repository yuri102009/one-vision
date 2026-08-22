from conexion import obtener_conexion


def consulta(consulta, parametros=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, parametros or ())
            resultados = cursor.fetchall()
        return resultados
    finally:
        conexion.close()



def insertar(consulta, parametros=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, parametros or ())
            conexion.commit()
        return 'Datos insertados correctamente'
    finally:
        conexion.close()