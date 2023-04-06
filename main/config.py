import os
import string
import random
import hashlib
import sys
from getpass import getpass

from utils.dbconfig import dbconfig #importing the dbconfig function 

from rich import print as printc
from rich.console import Console

console = Console()

def generateDeviceSecret(length = 10): # randomized characters used for salting the hash 
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))


def config(): # Initiate a Database 
    db = dbconfig() # Database object 
    cursor = db.cursor() # To execute db queries with the db cursor 

    try: # Try and except blook like this to handle exceptions in a more "rich" way
        cursor.execute("CREATE DATABASE pm") # The query to create a database 
    except Exception as e:
        printc("[red][!] An error occured while trying to create database!")
        console.print_exception(show_locals = True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created")


    # Create Table that will store the hash of the master password ---------------------------------------------------

    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)" 
    res = cursor.execute(query)         # cursor will execute the above query and print in green if successfully ran
    printc("[green][+][/green] Table 'secrets' created ")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)         # cursor will execute the above query and print in green if successfully ran
    printc("[green][+][/green] Table 'entries' created ")

    mp = "" #initiating MasterPassword
    while 1: #Creating a finite loop 
        mp = getpass("Choose a MASTER PASSWORD: ") # getpass, portable password input for python (Blank inputs)
        if mp == getpass("Retype: ") and mp != "": # If the masterpassword matches and it isn't blank 
            break # Breaks out of the while loop 
        printc("[yellow][-] Please try again. [/yellow]") # Otherwise keep trying. 

    # Hash the Master PASSWORD // Hash method will return the hash value of an object 
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest() # encode before hashing then use hexdigest to turn into its hexdecimal value 
                                                                    # hash.hexdigest()
                                                                    # Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits. 
                                                                    # This may be used to exchange the value safely in email or other non-binary environments
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    #Generate a DEVICE SECRET 
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device secret generated")

    # Insert the mastery password and the device secret together into the database 
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values(%s, %s)" # pm is the database name and secrets is the table name 
    val = (hashed_mp, ds)
    cursor.execute(query, val) # equivalent to these values (masterkey_hash, device_secret) values(%s, %s)
    db.commit() # inserting the values into the table

    printc("[green][+][/green] Added to the database")
    printc("[green][+] Configuration done. [/green]")

    db.close()


config()










printc("does it work?")
