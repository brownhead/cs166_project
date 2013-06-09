#!/usr/bin/env python

from flask import Flask
app = Flask("mnet")

import MySQLdb
db_connection = MySQLdb.connect(
	host = "cs166db.codecolorizer.com",
	user = "cs166user",
	passwd = "cs166pw",
	db = "cs166db"
)
db = db_connection.cursor()
