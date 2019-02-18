from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
#from utils.uiBuilder import printDetailledTrack # Uncomment for debug purpose only (printDetailledTrack() is very verbose)


# A Track container class
class Track:
    def __init__(self, fileType, pathList, fileName, audioTagPath):
        # ID3 tags
        self.title = ''
        self.artists = []
        self.albumTitle = ''
        self.year = ''
        self.performers = []
        self.composedPerformer = []
        self.composers = ''
        self.producer = ''
        self.trackNumber = ''
        self.totalTrack = ''
        self.discNumber = ''
        self.totalDisc = ''
        # Computed
        self.audioTagPath = audioTagPath
        self.audioTag = {}
        self.feat = []
        self.remix = []
        self.hasCover = False
        # Filesystem path and name as lists (separator is ` - `)
        self.pathList = pathList
        self.fileType = fileType
        self.fileName = fileName # Filename as a string
        self.fileNameList = [] # %releaseArtists% - %year% - %albumTitle% - %discNumber%%trackNumber% - %artists% - %title%
        self.folderNameList = [] # %year% - %albumTitle%
        # Self fill
        if fileType == 'MP3':
            self.audioTag = ID3(audioTagPath)
            self._fillFromMP3()
        elif fileType == 'FLAC':
            self.audioTag = FLAC(audioTagPath)
            self._fillFromFLAC()
        self._computeInternals()


    # Read the mp3 track ID3 tags and extract all interresting values into a Track object
    def _fillFromMP3(self):
        if 'TIT2' in self.audioTag and self.audioTag['TIT2'].text[0] != '':
            self.title = self.audioTag['TIT2'].text[0].rstrip()
        if 'TPE1' in self.audioTag:
            self.artists = self.audioTag['TPE1'].text[0].split('; ')
        if 'TALB' in self.audioTag:
            self.albumTitle = self.audioTag['TALB'].text[0].rstrip()
        if 'TDRC' in self.audioTag and self.audioTag['TDRC'].text[0].get_text() != '':
            self.year = self.audioTag['TDRC'].text[0].get_text()[:4].rstrip()
        if 'TPUB' in self.audioTag and self.audioTag['TPUB'].text[0] != '':
            self.producer = self.audioTag['TPUB'].text[0].rstrip()
        if 'TCOM' in self.audioTag and self.audioTag['TCOM'].text[0] != '':
            self.composers = self.audioTag['TCOM'].text[0]
        if 'TOPE' in self.audioTag and self.audioTag['TOPE'].text[0] != '':
            self.performers = self.audioTag['TOPE'].text[0].rstrip().split('; ')
        if 'TRCK' in self.audioTag and self.audioTag['TRCK'].text[0] != '':
            if '/' in self.audioTag['TRCK'].text[0]:
                tags = self.audioTag['TRCK'].text[0].rstrip().split('/')
                self.trackNumber = tags[0]
                self.totalTrack = tags[1]
            else:
                self.trackNumber = self.audioTag['TRCK'].text[0].rstrip()
        if 'TPOS' in self.audioTag and self.audioTag['TPOS'].text[0] != '':
            tags = self.audioTag['TPOS'].text[0].rstrip().split('/')
            self.discNumber = tags[0]
            if len(tags) > 1:
                self.totalDisc = tags[1]
            else:
                self.totalDisc = -1


    # Read the flac track Vorbis tags and extract all interresting values into a Track object
    def _fillFromFLAC(self):
        if 'TITLE' in self.audioTag:
            self.title = self.audioTag['TITLE'][0]
        if 'DATE' in self.audioTag:
            self.year = self.audioTag['DATE'][0]
        if 'TRACKNUMBER' in self.audioTag:
            self.trackNumber = self.audioTag['TRACKNUMBER'][0]
        if 'PRODUCER' in self.audioTag:
            self.producer = self.audioTag['PRODUCER'][0]
        if 'DISCNUMBER' in self.audioTag:
            self.discNumber = self.audioTag['DISCNUMBER'][0]
        if 'DISCTOTAL' in self.audioTag:
            self.totalDisc = self.audioTag['DISCTOTAL'][0]
        if 'TRACKTOTAL' in self.audioTag:
            self.totalTrack = self.audioTag['TRACKTOTAL'][0]
        if 'COMPOSER' in self.audioTag:
            self.composers = self.audioTag['COMPOSER'][0]
        if 'PERFORMER' in self.audioTag:
            self.performers = self.audioTag['PERFORMER'][0].split('; ')
        if 'ARTIST' in self.audioTag:
            self.artists = self.audioTag['ARTIST'][0].split('; ')
        if 'ALBUM' in self.audioTag:
            self.albumTitle = self.audioTag['ALBUM'][0]


    # Compute all class internals that can not be extracted from ID3 tags
    def _computeInternals(self):
        self._computeFileNameList()
        self._computeFolderNameList()
        self._computeFeaturing()
        self._computeRemixer()
        self._containsCover()


    # Splits the filename into its components (%releaseArtists% - %year% - %albumTitle% - %discNumber%%trackNumber% - %artists% - %title%)
    def _computeFileNameList(self):
        # We split the filename into its differents parts, as mentioned in this method description
        self.fileNameList = self.fileName.split(' - ')
        forbiddenPattern = ['Single', 'Intro', 'ÉPILOGUE']
        # Here we handle all specific cases (when ' - ' is not a separator)
        if len(self.fileNameList) > 6:
            if self.fileNameList[3] in forbiddenPattern: # When album is a single, we must re-join the album name and the 'Single' suffix
                self.fileNameList[2:4] = [' - '.join(self.fileNameList[2:4])] # Re-join with a ' - ' separator


    # Splits the folderame into its components (%year% - %albumTitle%)
    def _computeFolderNameList(self):
        # We also split the folder name to make a double check for Year and Album name
        self.folderNameList = self.pathList[len(self.pathList) - 1].split(' - ')
        forbiddenPattern = ['Single', 'Intro', 'ÉPILOGUE']

        if len(self.folderNameList) == 3:
            if self.folderNameList[2] in forbiddenPattern: # When album is a single, we must re-join the album name and the 'Single' suffix
                self.folderNameList[1:3] = [' - '.join(self.folderNameList[1:3])] # Re-join with a ' - ' separator


    # Extract the featured artist(s) name(s) from the track fileName
    def _computeFeaturing(self):
        if self.fileName.find('(feat.') != -1:
            startIndex = self.fileName.rfind('(feat.', 0, len(self.fileName))
            self.feat = self.fileName[startIndex+7:self.fileName.find(')', startIndex)].split(', ') # +7 is to remove the `(feat. ` string from feat artist
            if len(self.feat) > 0 and self.feat[0] != '':
                self.composedPerformer = [*self.feat, *self.artists]
                return
        self.composedPerformer = self.artists

    # Extract the track remix artist name from the track fileName
    def _computeRemixer(self):
        if self.fileName.find(' Remix)') != -1:
            self.remix = self.fileName[self.fileName.rfind('(', 0, len(self.fileName))+1:self.fileName.rfind(' Remix)')].split(', ') # +1 is to remove the opening parenthesis


    # Test the cover existence in the file
    def _containsCover(self):
        frontPicture = {}
        # Extract image from file
        if self.fileType == 'MP3' and 'APIC:' in self.audioTag:
            frontPicture = self.audioTag['APIC:'].data
        elif self.fileType == 'FLAC':
            frontPicture = self.audioTag.pictures
        # Test cover existence
        if len(frontPicture) != 0:
            self.hasCover = True
        else:
            self.hasCover = False
