class Accessor():
    
    # GET: Return all school resources. No autorizations
	#
	# Example request: curl -i -H "Content-Type: application/json" -X GET
	# -b cookie-jar -k https://192.168.10.4:61340/schools
	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getSchools'
			cursor = dbConnection.cursor()
			cursor.callproc(sql) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'schools': rows}), 200) # turn set into json and return it