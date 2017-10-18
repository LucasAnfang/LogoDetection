from log_entries_base import LogEntriesBase

class InputLogEntries(LogEntriesBase):
    """ Keys """
    """ PATH is coming from parent class """
    PATH = 'path'
    PROCESSING_STATUS = 'Processing_Status'
    PROCESSED = 'Processed'
    UNPROCESSED = 'Unprocessed'

    def __init__(self, filename = 'log.txt'):
        LogEntriesBase.__init__(self, filename)

    def get_logs(self, isProcessed = None):
        if(isProcessed == None):
            filter = None
        else:
            processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
            filter = { InputLogEntries.PROCESSING_STATUS : processing_status }
        return LogEntriesBase.get_logs(self, filter = filter)

    def update(self, path, isProcessed):
        processing_status = InputLogEntries.PROCESSED if isProcessed else InputLogEntries.UNPROCESSED
        entry = { LogEntriesBase.PATH : path, InputLogEntries.PROCESSING_STATUS : processing_status }
        LogEntriesBase.update(self, entry)
