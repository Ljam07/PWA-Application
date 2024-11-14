from DBApi import DataBase

############ Main logic ###############

# Connect to db
user = DataBase("src/DB/users.db")

# Execute instruction
user.DBExecute("CREATE TABLE users (email TEXT, username TEXT\
, first TEXT, last TEXT, password CHAR, permissions TINYINT)")

#Close db
user.DBClose()


### Same thing but for games database
games = DataBase("src/DB/games.db")
games.DBExecute("CREATE TABLE games (title TEXT, year int, rating INT)")
games.DBClose()