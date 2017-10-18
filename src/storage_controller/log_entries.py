import json

PREFIX = 'Prefix'
PROCESSING_STATUS = 'Processing_Status'
PROCESSED = 'Processed'
UNPROCESSED = 'Unprocessed'

class LogEntries:
	def __init__(self):
		self.log_entries = []

	def append(self, prefix, isProcessed):
		processing_status = PROCESSED if isProcessed else UNPROCESSED
		dictionary = {}
		dictionary[PREFIX] = prefix
		dictionary[PROCESSING_STATUS] = processing_status
		self.log_entries.append(dictionary)

	def update(self, prefix, isProcessed):
		processing_status = PROCESSED if isProcessed else UNPROCESSED
		if(len([x for x in self.log_entries if x[PREFIX] == prefix]) == 0):
			self.append(prefix, isProcessed)
		else:
			entry = [x for x in self.log_entries if x[PREFIX] == prefix]
			entry[0][PROCESSING_STATUS] = processing_status

	def GetLogs(self, processing_status_filter = None):
		if(processing_status_filter == None):
			return self.log_entries
		return [x for x in self.log_entries if x[PROCESSING_STATUS] == processing_status_filter]

	def GetUnprocessedBlobNames(self):
		# return [x[UNPROCESSED] for x in self.log_entries if x[PROCESSING_STATUS] == UNPROCESSED]
		return [x[PREFIX] for x in self.log_entries if x[PROCESSING_STATUS] == UNPROCESSED]

	def serialize(self):
		return json.dumps(self.log_entries, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.log_entries = json.loads(serialized_entity)
