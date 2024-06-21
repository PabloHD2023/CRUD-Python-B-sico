import mysql.connector

#Conección a la BDD
database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'prueba_python_bdd',
)