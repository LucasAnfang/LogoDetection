from log_entries_base import LogEntriesBase

class InputLogEntries(LogEntriesBase):
    """ Keys """
    """ PATH is coming from parent class """
    PROCESSING_STATUS = 'Processing_Status'
    PROCESSED = 'Processed'
    UNPROCESSED = 'Unprocessed'

    def __init__(self, filename = 'log.txt'):
        LogEntriesBase.__init__(self, filename)

    def get_logs(self, isProcessed = None):
        if(isProcessed == None):
            filter = None
        else:
            processing_status = PROCESSED if isProcessed else UNPROCESSED
            filter = { PROCESSING_STATUS : processing_status }
        return LogEntriesBase.get_logs(self, filter = filter)

	def update(self, path, isProcessed):
        processing_status = PROCESSED if isProcessed else UNPROCESSED
        entry = { LogEntriesBase.PATH : path, PROCESSING_STATUS : processing_status }
        LogEntriesBase.update(self, entry)
