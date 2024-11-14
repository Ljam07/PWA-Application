import sqlite3
import sys

class DataBase:
    def __init__(self, location):
        self.connection = self.DBConnect(location)

    ## Main error handling function
    def ErrorHandle(self, error = None):
        #Given feedback before close
        if error:
            sys.exit(f"An error occured: {error}.")
        #Close with no feedback
        else:
            sys.exit("An error occured. No feedback given.")

    # Create/Connect to dabatase
    def DBConnect(self, location):
        try:
            conn = sqlite3.connect(location)
            print("Connected to database successfully.") 
            return conn
        except Exception as e:
            self.ErrorHandle(f"Could not connect to database, {e}")

    # Execute instructions
    def DBExecute(self, instruction):
        try:
            self.connection.execute(instruction)
            print("Instructions executed successfully.") 
        except Exception as e:
            self.ErrorHandle(f"Could not execute instructions, {e}")

    # Close database
    def DBClose(self):
        try:
            self.connection.close()
            print("Closed Database")
        except Exception as e:
            self.ErrorHandle(f"Could not close database, {e}")