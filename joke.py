import requests
import json

def joke():
	t = requests.get("http://joke.deno.dev").text
	j = json.loads(t)
	"""
	id = j["id"]
	type = j["type"]
	setup = j["setup"]
	punchline = j["punchline"]
	"""
	return j
	
	
	
joke()