import json

INTERACTING_ENTITY = 'Interacting_Entity'
ACTION = 'Action'
PATH = 'Path'
PROCESSING_STATUS = 'Processing_Status'
PROCESSED = 'Processed'
UNPROCESSED = 'Unprocessed'

class LogEntries:
	def __init__(self):
		self.log_entries = []

	def append(self, interacting_entity, action, path, processing_status):
		dictionary = {}
		dictionary[INTERACTING_ENTITY] = interacting_entity
		dictionary[ACTION] = action
		dictionary[PATH] = path
		dictionary[PROCESSING_STATUS] = processing_status
		self.log_entries.append(dictionary)

	def serialize(self):
		return json.dumps(self.log_entries, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.log_entries = json.loads(serialized_entity)

