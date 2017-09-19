import json

PATH = 'Path'
PROCESSING_STATUS = 'Processing_Status'
PROCESSED = 'Processed'
UNPROCESSED = 'Unprocessed'

class LogEntries:
	def __init__(self):
		self.log_entries = []

	def append(self, path, isProcessed):
		processing_status = PROCESSED if isProcessed else UNPROCESSED 
		dictionary = {}
		dictionary[PATH] = path
		dictionary[PROCESSING_STATUS] = processing_status
		self.log_entries.append(dictionary)

	def update(self, path, isProcessed):
		processing_status = PROCESSED if isProcessed else UNPROCESSED
		if(len([x for x in self.log_entries if x[PATH] == path]) == 0):
			self.append(path, isProcessed)
		else:
			entry = [x for x in self.log_entries if x[PATH] == path]
			entry[PROCESSING_STATUS] = processing_status

	def GetLogs(self, processing_status_filter = None):
		if(processing_status_filter == None):
			return self.log_entries
		return [x for x in self.log_entries if x[PROCESSING_STATUS] == processing_status_filter]

	def serialize(self):
		return json.dumps(self.log_entries, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.log_entries = json.loads(serialized_entity)

