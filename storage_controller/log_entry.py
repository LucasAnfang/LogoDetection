# from complex_encoder import ComplexEncoder
import json

class ComplexEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, LogEntry):
			return obj.__dict__ 
		if isinstance(obj, LogEntries):
			return obj.__dict__ 
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)

class LogEntry:
	def __init__(self, Interacting_Entity, Action, Path):
		self.Interacting_Entity = Interacting_Entity
		self.Action = Action
		self.Path = Path

	def serialize(self):
		return json.dumps(self, cls=ComplexEncoder)

class LogEntries:
	def __init__(self):
		self.Logs = []

	def append(self, logEntry):
		self.Logs.append(logEntry)

	def serialize(self):
		return json.dumps(self, cls=ComplexEncoder)
