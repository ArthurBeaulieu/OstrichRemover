from utils.uiBuilder import printDetailledTrack


# A Track container class
class Track:
    def __init__(self, fileTye, pathList, fileName, audioTag):
        # ID3 tags
        self.title = ''
        self.artists = ''
        self.albumTitle = ''
        self.year = ''
        self.performers = ''
        self.composers = ''
        self.producer = ''
        self.trackNumber = ''
        self.trackTotal = ''
        self.discNumber = ''
        self.discTotal = ''
        # Computed
        self.remix = ''
        self.feat = ''
        # Filesystem path and name as lists (separator is ` - `)
        self.pathList = pathList
        self.fileTye = fileTye
        self.fileName = fileName # Filename as a string
        self.fileNameList = [] # %releaseArtists% - %year% - %albumTitle% - %discNumber%%trackNumber% - %artists% - %title%
        self.folderNameList = [] # %year% - %albumTitle%
        # Data collection
        self.errors = [] # TODO insert in it items that are in the errorEnum
        # Self fill
        if fileTye == 'MP3':
            self._fillFromMP3(audioTag)
        elif fileTye == 'FLAC':
            self._fillFromFLAC(audioTag)
        self._computeInternals()
        printDetailledTrack(self)


    # Read the mp3 track ID3 tags and extract all interresting values into a Track object
    def _fillFromMP3(self, audioTag):
        if 'TIT2' in audioTag and audioTag['TIT2'].text[0] != '':
            self.title = audioTag['TIT2'].text[0].rstrip()
        if 'TPE1' in audioTag:
            self.artists = audioTag['TPE1'].text[0]
        if 'TALB' in audioTag:
            self.albumTitle = audioTag['TALB'].text[0].rstrip()
        if 'TDRC' in audioTag and audioTag['TDRC'].text[0].get_text() != '':
            self.year = audioTag['TDRC'].text[0].get_text()[:4].rstrip()
        if 'TPUB' in audioTag and audioTag['TPUB'].text[0] != '':
            self.producer = audioTag['TPUB'].text[0].rstrip()
        if 'TCOM' in audioTag and audioTag['TCOM'].text[0] != '':
            self.composers = audioTag['TCOM'].text[0]
        if 'TOPE' in audioTag and audioTag['TOPE'].text[0] != '':
            self.performers = audioTag['TOPE'].text[0].rstrip()
        if 'TRCK' in audioTag and audioTag['TRCK'].text[0] != '':
            if '/' in audioTag['TRCK'].text[0]:
                tags = audioTag['TRCK'].text[0].rstrip().split('/')
                self.trackNumber = tags[0]
                self.trackTotal = tags[1]
            else:
                self.trackNumber = audioTag['TRCK'].text[0].rstrip()
        if 'TPOS' in audioTag and audioTag['TPOS'].text[0] != '':
            tags = audioTag['TPOS'].text[0].rstrip().split('/')
            self.discNumber = tags[0]
            if len(tags) > 1:
                self.discTotal = tags[1]
            else:
                self.discTotal = -1


    # Read the flac track Vorbis tags and extract all interresting values into a Track object
    def _fillFromFLAC(self, audioTag):
        if 'TITLE' in audioTag:
            self.title = audioTag['TITLE'][0]
        if 'DATE' in audioTag:
            self.year = audioTag['DATE'][0]
        if 'TRACKNUMBER' in audioTag:
            self.trackNumber = audioTag['TRACKNUMBER'][0]
        if 'PRODUCER' in audioTag:
            self.producer = audioTag['PRODUCER'][0]
        if 'DISCNUMBER' in audioTag:
            self.discNumber = audioTag['DISCNUMBER'][0]
        if 'TOTALDISC' in audioTag:
            self.totalDisc = audioTag['TOTALDISC'][0]
        if 'TOTALTRACK' in audioTag:
            self.totalTrack = audioTag['TOTALTRACK'][0]
        if 'COMPOSER' in audioTag:
            self.composers = audioTag['COMPOSER'][0]
        if 'PERFORMER' in audioTag:
            self.performers = audioTag['PERFORMER'][0]
        if 'ARTIST' in audioTag:
            self.artists = audioTag['ARTIST'][0]
        if 'ALBUM' in audioTag:
            self.albumTitle = audioTag['ALBUM'][0]


    def _computeInternals(self):
        self._computeFileNameList()
        self._computeFolderNameList()
        self._computeRemixer()
        self._computeFeaturing()


    # Splits the filename into its components (%releaseArtists% - %year% - %albumTitle% - %discNumber%%trackNumber% - %artists% - %title%)
    def _computeFileNameList(self):
        # We split the filename into its differents parts, as mentioned in this method description
        self.fileNameList = self.fileName.split(' - ')
        # TODO mk list of forbidden patterns
        # Here we handle all specific cases (when ' - ' is not a separator)
        if len(self.fileNameList) > 6:
            if self.fileNameList[3] == 'Single' or self.fileNameList[3] == 'ÉPILOGUE': # When album is a single, we must re-join the album name and the 'Single' suffix
                self.fileNameList[2:4] = [' - '.join(self.fileNameList[2:4])] # Re-join with a ' - ' separator


    # Splits the folderame into its components (%year% - %albumTitle%)
    def _computeFolderNameList(self):
        # We also split the folder name to make a double check for Year and Album name
        self.folderNameList = self.pathList[len(self.pathList) - 1].split(' - ')
        if len(self.folderNameList) == 3:
            if self.folderNameList[2] == 'Single' or self.folderNameList[2] == 'ÉPILOGUE': # When album is a single, we must re-join the album name and the 'Single' suffix
                self.folderNameList[1:3] = [' - '.join(self.folderNameList[1:3])] # Re-join with a ' - ' separator


    # Extract the track remix artist name from the track fileName
    def _computeRemixer(self):
        if self.fileName.find(' Remix)') != -1:
            self.remix = self.fileName[self.fileName.rfind('(', 0, len(self.fileName))+1:self.fileName.find(' Remix)')] # +1 is to remove the opening parenthesis


    # Extract the featured artist(s) name(s) from the track fileName
    def _computeFeaturing(self):
        if self.fileName.find('(feat.') != -1:
            self.feat = self.fileName[self.fileName.rfind('(feat.', 0, len(self.fileName))+7:self.fileName.find(')')] # +7 is to remove the `(feat. ` string from feat artist
