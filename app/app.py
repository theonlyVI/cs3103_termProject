#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql
import pymysql.cursors
import ssl #include ssl libraries
import cgi
import cgitb
import settings # Our server and db settings, stored in settings.py
from werkzeug.utils import secure_filename
import os
from datetime import datetime


cgitb.enable()
app = Flask(__name__, static_url_path='/static')


#CORS(app)
# Set Server-side session config: Save sessions in the local app directory.
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
app.config['UPLOAD_FOLDER'] = 'static/resources/videos/'

Session(app)


####################################################################################
# Error handlers

@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

@app.errorhandler(500) # decorators to add to 500 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Internal server error' } ), 500)


####################################################################################
# Routing: GET and POST using Flask-Session

class Root(Resource):
	def get(self):
		# return make_response('no data')
		return app.send_static_file('homepage.html')

class LogIn(Resource):

	# Set Session and return Cookie
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Rick", "password": "crapcrap"}'
	#  	-c cookie-jar -k https://192.168.10.4:61340/signin

	def post(self):

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.

				session['username'] = request_params['username']
				
				# Stuff in here to find the esiting userId or create a use and get the created userId
				response = {'status': 'success', 'user_id':'1' }
				responseCode = 201
				call('createUser', True, (session['username'],))
			except LDAPException:
				response = {'status': 'Access denied'}
				print(response)
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET
	#	-b cookie-jar -k https://192.168.10.4:61340/login
	def get(self):
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)
	
class LogOut(Resource):
	# DELETE: Logout: remove session
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	http://info3103.cs.unb.ca:61340/logout

	def delete(self):
		if 'username' in session:
			session.pop('username', None)
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'success'}
			responseCode = 204
		return make_response(jsonify(response), responseCode)
	
class Users(Resource):
	# GET: info of all users
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET
	#	-b cookie-jar -k https://192.168.10.4:8017/Users
	def get(self):
		response = call('getUserList')
		responseCode = 200
		return make_response(jsonify(response), responseCode)

class loggedInUser(Resource):
	# GET: info of all users
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET
	#	-b cookie-jar -k https://192.168.10.4:8017/Users
	def get(self, username):
		if 'username' in session:
			username = session['username']
			response = call('getUserInfo', True, (username,))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	def delete(self, username):
		if 'username' in session and username == session['username']:
			response = call('deleteUser', True, (username,))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

class loggedInUserComment(Resource):
	# GET: info of all users
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET
	#	-b cookie-jar -k https://192.168.10.4:8017/Users
	def get(self, username):
		if 'username' in session and username == session['username']:
			response = call('getCommentsByUser', True, (username,))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	def post(self, username):
		if 'username' in session and username == session['username']:
			response = call('writeComment', True, (username, request.args.get('video_id'), request.form['comment'],))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)
	


class loggedInUserCommentManip(Resource):

	def get(self, username, comment_id):
		print(session)
		if 'username' in session and username == session['username']:
			response = call('getCommentByIdAndUser', True, (username, comment_id,))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

	def patch(self, username, comment_id):
		if 'username' in session and username == session['username']:
			response = call('editComment', True, (username, comment_id, request.form['comment'],))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)
	
	def delete(self, username, comment_id):
		if 'username' in session and username == session['username']:
			response = call('getCommentByIdAndUser', True, (username, comment_id,))
			call('deleteComment', True, (username, comment_id,))
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)
	

###########################################################
# ALI's CODE

class VideoGen(Resource):
	def get(self):
		response = call('getAllVideos')
		responsecode = 200
		if len(response) < 0:
			return make_response(jsonify({"status": "fail"}), 404)
		return make_response(jsonify(response), responsecode)

class VideoId(Resource):
	def get(self, videoId):
		sqlargs = (videoId,)
		response = call('getVideo', True, sqlargs)
		if len(response) < 0:
			return make_response(jsonify({"status": "fail"}), 404)
		responsecode = 200
		return make_response(jsonify(response), responsecode)


class VidCom(Resource):
	def get(self, videoId):
		sqlargs = (videoId,)
		response = call('getCommentsList', True, sqlargs)
		responsecode = 200
		return make_response(jsonify(response), responsecode)

class VidUse(Resource):
	# get videos of the currently logged in users
	# curl command: curl -X GET -b cookie-jar http://cs3103.cs.unb.ca:8017/Users/{username}/Videos
	def get(self, username):
		sqlargs = (username, )
		response = call('getVideoList', True, sqlargs)
		# if len(response) < 0:
		# 	return make_response(jsonify({"status": "fail"}), 404)
		responsecode = 200
		return make_response(jsonify(response), responsecode)
	

	def post(self, username):
		if 'username' in session and username == session['username']:
			title = request.form['title']
			description = request.form['description']
			file = request.files['file']
			filename = secure_filename(username + '_' + file.filename)
			save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(save_path)
			try:
				call('uploadVideo', True, (username, title, description, save_path,))
				message = {"status": "success"}
				responseCode = 200
			except Exception as e:
				print(e)
				message = {"status": "fail to upload Video"}
				responseCode = 400

		return make_response(jsonify(message), responseCode)
	


class VidLiked(Resource):
	def get(self, username):
		sqlargs = (username, )
		response = call('getLikedVideos', True, sqlargs)
		if len(response) < 0:
			return make_response(jsonify({"status": "fail"}), 404)
		responsecode = 200
		return make_response(jsonify(response), responsecode)


class ViDel(Resource):
	def delete(self, username, videoId):
		if 'username' in session and username == session['username']:
			sqlargs = (username, videoId,)
			response = call('deleteVideo', True, sqlargs)
			responsecode = 200
			return make_response(jsonify(response), responsecode)
		else:
			return make_response(jsonify({"status": "fail"}), 403)


class VidLik(Resource):
	def post(self, username, videoId):
		if 'username' in session and username == session['username']:		
			sqlargs = (username, videoId, )
			response = call('likeVideo', True, sqlargs)
			responsecode = 200
			return make_response(jsonify("video id " + str(videoId) +  " Liked"), responsecode)
		else:
			return make_response(jsonify({"status": "fail"}), 403)
	
	def delete(self, username, videoId):
		if 'username' in session:
			sqlargs = (username, videoId, )
			response = call('removeLike', True, sqlargs)
			responsecode = 200
			return make_response(jsonify("like deleted"), responsecode)
		else:
			return make_response(jsonify({"status": "fail"}), 403)


####################################################################################

class VidLikeCount(Resource):
	def get(self, videoId):
		try:
			response = call('getLikeCount', True, (videoId,))
			responseCode = 200
		except Exception as e:
			response = {'status': 'fail'}
			responseCode = 400
		return make_response(jsonify(response), responseCode)


####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Root,'/')
# api.add_resource(Developer,'/dev')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(Users, '/Users')
api.add_resource(loggedInUser, '/Users/<string:username>')
api.add_resource(loggedInUserComment, '/Users/<string:username>/Comments')
api.add_resource(loggedInUserCommentManip, '/Users/<string:username>/Comments/<int:comment_id>')

# ALI's part
api.add_resource(VideoGen, '/Videos')
api.add_resource(VideoId, '/Videos/<int:videoId>')
api.add_resource(VidCom, '/Videos/<int:videoId>/Comments')
api.add_resource(VidUse, '/Users/<string:username>/Videos')
api.add_resource(VidLiked, '/Users/<string:username>/Videos/Liked')
api.add_resource(ViDel, '/Users/<string:username>/Videos/<int:videoId>')
api.add_resource(VidLik, '/Users/<string:username>/Videos/<int:videoId>/Like')
api.add_resource(VidLikeCount, '/Videos/<int:videoId>/Like/Count')


#####################################################################################
# Create database connection
def call(proc_name: str, have_args=False, sqlArgs=()):
	try:
		dbConnection = pymysql.connect(
		settings.DB_HOST,
		settings.DB_USER,
		settings.DB_PASSWD,
		settings.DB_DATABASE,
		charset='utf8mb4',
		cursorclass= pymysql.cursors.DictCursor)
		cursor = dbConnection.cursor()
		# try:
		if have_args:
			cursor.callproc(proc_name, sqlArgs)
			dbConnection.commit()
		else:
			cursor.callproc(proc_name) # stored procedure, no arguments
			dbConnection.commit()
		rows = cursor.fetchall() # get all the results
		# except pymysql.err as e:
		# 	rows = {'error': str(e)}
	except Exception as e:
		rows = {'error': str(e)}
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
		return rows # turn set into json and return it

#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)