from DBApi import *

############ Main logic ###############

# Connect to db
conn = DBConnect("src/DB/users.db")

# Execute instruction
DBExecute(conn, "CREATE TABLE users (email TEXT, username TEXT\
, first TEXT, last TEXT, password TEXT, permissions TINYINT)")

#Close db
DBClose(conn)