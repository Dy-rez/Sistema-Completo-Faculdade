import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # seu usuário MySQL
        password="123456",   # sua senha do MySQL
        database="gerenciamento_notas"
    )
