import json

PATH = 'path'

class LogEntriesBase:
	def __init__(self):
		self.ResetLogs()

	def append(self, entry):
		if PATH in entry:
			self.log_entries.append(entry)

	def update(self, entry):
		if PATH in entry:
			if(len([log_entry for log_entry in self.log_entries if log_entry[PATH] == entry[PATH]]) == 0):
				self.append(entry)
			else:
				entries = [log_entry for log_entry in self.log_entries if log_entry[PATH] == entry[PATH]]
				entries[0].update(entry)

	def GetLogs(self, filter = None):
		if(filter == None):
			return self.log_entries
		return [log_entry for log_entry in self.log_entries if filter.viewitems() <= log_entry.viewitems()]

	def ResetLogs(self):
		self self.log_entries = []

	def serialize(self):
		return json.dumps(self.log_entries, indent=4, sort_keys=True, ensure_ascii=False)

	def deserialize(self, serialized_entity):
		self.log_entries = json.loads(serialized_entity)
