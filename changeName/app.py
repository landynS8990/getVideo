import requests
from flask import Flask, jsonify, render_template
import asyncio
import threading
import time
import os
from ytTest import get_authenticated_service, update_video
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

viewCnt = 0
app = Flask(__name__)
def onlyNumbs(strin):
	kArr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	jStr = ""
	for h in strin:
		if h in kArr:
			jStr += h
	return jStr

def getViews():
	x = requests.get('VIDEO_URL')
	s1 = str(x.text)
	g = s1.split("shortViewCount",1)[0]
	b = g.split("videoViewCountRenderer",1)[1]
	viewCount = int(onlyNumbs(b))
	return viewCount

def thread_function(name):
	global viewCnt
	dj = 0
	j = 0
	while j < 10:
		dj = 0
		mns = getViews()
		print(viewCnt)
		print(mns)
		if viewCnt == mns:
			dj = 0
		else:
			viewCnt = mns
			b = requests.get('https://APP_NAME.herokuapp.com/ytB')
			dj = 1
		time.sleep(10)
		j += 1
	x = requests.get('https://APP_NAME.herokuapp.com/')


@app.route('/')
def index():
	h = 0
	x = threading.Thread(target=thread_function, args=(1,))
	x.start()
	return jsonify({"result": h})

@app.route('/ytB')
def ytB():
	youtube = get_authenticated_service()
	print(youtube)
	getV = getViews()
	viewString = f'{getV} views on this video'
	update_video(youtube, viewString)
	return jsonify({"result": viewString})

if __name__ == "__main__":
	app.run()