import sqlite3
import sys

## Main error handling function
def ErrorHandle(error = None):
    #Given feedback before close
    if error:
        sys.exit(("Fatal error occured: ", error))
    #Close with no feedback
    else:
        sys.exit("Fatal error occured. No feedback given.")

# Create/Connect to dabatase
def DBConnect(location):
    try:
        conn = sqlite3.connect(location)
        print("Connected to database successfully.") 
        return conn
    except Exception as e:
        ErrorHandle(f"Could not connect to database, {e}")

# Execute structions
def DBExecute(location, instruction):
    try:
        location.execute(instruction)
        print("Instructions executed successfully.") 
    except Exception as e:
        ErrorHandle(f"Could not execute instructions, {e}")

# Close database
def DBClose(location):
    try:
        location.close()
        print("Closed Database")
    except Exception as e:
        ErrorHandle(f"Could not close database, {e}")