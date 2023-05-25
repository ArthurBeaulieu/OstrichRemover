# An Album container class with all useful attributes
class Album(object):
    def __init__(self, filesIterable):
        self.filesIterable = filesIterable
        self.folderNameList = [] # %year%, %albumTitle%
        self.albumTitle = ''
        self.albumArtist = ''
        self.totalTrack = 0
        self.totalDisc = '1'
        self.year = 0
        self.label = ''
        self.genres = []
        self.compilation = 0
        self.lang = ''
        self.hasCover = False
        self.coverName = ''
