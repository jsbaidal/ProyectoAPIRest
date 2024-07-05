import pyodbc 

# Establishing a connection to the SQL Server

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-OC8AB8O\\SQLEXPRESS;DATABASE=testDB;')
                
print("conexion")

cursor = conn.cursor()

# Query para seleccionar todos los registros de la tabla 'equipos'
query = "SELECT * FROM equipos"

try:
    # Ejecutar el query usando el cursor
    cursor.execute(query)

    # Obtener todos los resultados del cursor
    rows = cursor.fetchall()

    # Imprimir o procesar los resultados según sea necesario
    for row in rows:
        print(row)  # Imprime cada fila, puedes ajustar esto según tu necesidad

except Exception as e:
    print(f"Error al ejecutar el query: {e}")

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()