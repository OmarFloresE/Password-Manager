import mysql.connector # Importing MySQL database driver 

from rich import print as printc
from rich.console import Console 
console = Console() # Using rich print libaries console instance

def dbconfig(): # Function that initializes the database (Like a constructor)
    try:
        db = mysql.connector.connect(
            host = 'localhost',
            user = 'pm',
            passwd = 'password'
        )
    except Exception as e: # To access the atributes of the exception object  
        console.print_exception(show_locals=True)

    return db # returning the database object