from utilities.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()

def struct(): # Initiate a Database 
    db = dbconfig()
    cursor = db.cursor()

    try: 
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] An error occured while trying to create database!")
        console.print_exception(show_locals = True)

Print("so far so good.")
