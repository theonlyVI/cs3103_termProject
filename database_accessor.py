#!/usr/bin/env python3
import sys
import json
import pymysql
import pymysql.cursors
from flask import jsonify

import settings


class Accessor():
	def __init__(self) -> None:
		self.host = settings.APP_HOST
		self.user = settings.DB_USER
		self.psw = settings.DB_PASSWD
		self.db = settings.DB_DATABASE
		charset = 'utf8mb4'

	def call(self, proc_name: str, have_args: bool, args=()):
    # GET: Return all school resources. No autorizations
	#
	# Example request: curl -i -H "Content-Type: application/json" -X GET
	# -b cookie-jar -k https://192.168.10.4:61340/schools
		try:
			dbConnection = pymysql.connect(self.host, 
				self.user, 
				self.psw, 
				self.db, 
				self.charset, 
				cursorclass= pymysql.cursors.DictCursor)
			cursor = dbConnection.cursor()
			if have_args:
				cursor.callproc(proc_name, args)
			else:
				cursor.callproc(proc_name) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
		except Exception as e:
			return(e) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return jsonify(rows) # turn set into json and return it