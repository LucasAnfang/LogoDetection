import json

class ComplexEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, P):
			return obj.__dict__ 
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)

