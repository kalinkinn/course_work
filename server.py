import time
from datetime import datetime

from flask import Flask, request


app = Flask(__name__)

db = [
	{
		'name': 'TestUser_1',
		'text': 'Sample text',
		'time': time.time()
	}, {
		'name': 'TestUser_2',
		'text': 'Sample text',
		'time': time.time()
	}
]


@app.route("/")
def test():
	return 'Server is working fine, my little pogchamp UWU'

@app.route("/status")
def status():
	dt = datetime.now()
	return {
		'status': True,
		'name': 'Messenger',
		'time': time.time(),
		'time1': time.asctime(),
		'time2': dt,
		'time3': str(dt),
		'time4': dt.strftime('%Y/%m/%d %H:%M'),
		'time5': dt.isoformat(),
		'time6': datetime.utcnow().isoformat(),
	}

@app.route("/send", methods = ['POST'])
def send_message():
	if not isinstance(request.json, dict):
		return abort(400)
	name = request.json['name']
	text = request.json['text']
	if not (isinstance(name, str) and isinstance(text, str) and name and text):
		return 400
	new_message = {
		'name': name,
		'text': text,
		'time': time.time()
	}
	db.append(new_message)

	return {'ok': True}

@app.route("/messages")
def get_messages():
	try:
		after = float(request.args.get('after', 0))
	except ValueError:
		return abort(400)
	messages = []
	for message in db:
		if message['time'] > after:
			messages.append(message)
	return {'messages': messages}

app.run()