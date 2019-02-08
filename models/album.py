class Album:
    def __init__(self, filesIterable):
        self.filesIterable = filesIterable
        self.folderNameList = [] # %year% - %albumTitle%        
        self.trackTotal = 0
        self.discTotal = 1
        self.year = 0
