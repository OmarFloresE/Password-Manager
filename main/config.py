import os
import string
import random
import hashlib
import sys
from getpass import getpass

from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()

def config(): # Initiate a Database 
    db = dbconfig()
    cursor = db.cursor()

    try: 
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] An error occured while trying to create database!")
        console.print_exception(show_locals = True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created")

    # Create Tables 
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)" #masterpass? 
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created ")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created ")

    mp = ""
    while 1:
        mp = getpass("Choose a MASTER PASSWORD: ")
        if mp == getpass("Retype: ") and mp != "": # error error error
            break
        printc("[yellow][-] Please try again. [/yellow]")

    # Hash the Master PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    #Generate a DEVICE SECRET 
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device secret generated")

    # Add them to DB
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values(%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()


config()










printc("does it work?")
