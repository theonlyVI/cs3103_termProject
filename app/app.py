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

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__)
#CORS(app)
# Set Server-side session config: Save sessions in the local app directory.
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST

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

#			if request_params['username'] == 'Rick' and request_params['password'] == 'crapcrap':
#				session['username'] = request_params['username']
#				response = {'status': 'success', 'user_id':'1'}
#				responseCode = 201
#			else:
#				response = {'status': 'Access denied'}
#				responseCode = 403

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
			json_data = request.get_json()
			response = call('writeComment', True, (username, request.args.get('video_id'), json_data.get('comment'),))
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
			json_data = request.get_json()
			response = call('editComment', True, (username, comment_id, json_data.get('comment'),))
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
	def get(self, username):
		sqlargs = (username, )
		response = call('getVideoList', True, sqlargs)
		# if len(response) < 0:
		# 	return make_response(jsonify({"status": "fail"}), 404)
		responsecode = 200
		return make_response(jsonify(response), responsecode)
	

	def post(self, username):
		if not request.json or not 'Path' in request.json:
			abort(400)
		if 'username' in session and username == session['username']:
			vPath = request.json['Path']
			vTitle = request.json['Title']
			vDesc = request.json['Description']
			sqlargs = (username, vTitle, vDesc, vPath,)
			response = call('uploadVideo', True, sqlargs)
			responsecode = 200
			return make_response(jsonify(response), responsecode)
		return make_response(jsonify({"status": "fail"}), 403)

class VidLiked(Resource):
	def get(self, userId):
		sqlargs = (userId, )
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




####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
# api.add_resource(Root,'/')
# api.add_resource(Developer,'/dev')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(Users, '/Users')
api.add_resource(loggedInUser, '/Users/<string:username>')
api.add_resource(loggedInUserComment, '/Users/<string:username>/Comments')
api.add_resource(loggedInUserCommentManip, '/Users/<string:username>/Comments/<int:comment_id>')

# ALI's part
api.add_resource(VideoGen, '/videos')
api.add_resource(VideoId, '/videos/<int:videoId>')
api.add_resource(VidCom, '/videos/<int:videoId>/comments')
api.add_resource(VidUse, '/users/<string:username>/videos')
api.add_resource(VidLiked, '/users/<int:userId>/videos/liked')
api.add_resource(ViDel, '/users/<string:username>/videos/<int:videoId>')
api.add_resource(VidLik, '/users/<string:username>/videos/<int:videoId>/like')


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