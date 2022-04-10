import mysql.connector

# DB configurations
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Abc12345!',
    db = 'pharm_store',
    autocommit = True
)
