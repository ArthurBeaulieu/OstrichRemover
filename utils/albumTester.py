from models.album import Album
from models.track import Track
from utils.trackTester import TrackTester
from utils.errorEnum import ErrorEnum


class AlbumTester:
    def __init__(self, files, preservedPath):
        self.preservedPath = preservedPath
        self.files = files
        self.album = Album(files)
        self.tracks = []
        self.errors = []
        self.errorCounter = 0
        self.trackErrors = []
        self.missingTags = []
        self.missingTagsCounter = 0
        self.missorderedTag = []
        self.missorderedTagsCounter = 0
        self._analyseAlbumInternals()
        self._analyseTracks()


    def _analyseAlbumInternals(self):
        lockErrors = False
        for fileName in self.album.filesIterable:
            if fileName[-3:] == 'MP3' or fileName[-3:] == 'mp3' or fileName[-4:] == 'FLAC' or fileName[-4:] == 'flac':
                self.album.totalTrack += 1
                fileNameList = fileName.split(' - ')
                if len(fileName) == 6 and int(fileNameList[len(fileNameList) - 3][:-2]) > int(self.album.totalDisc):
                    self.album.totalDisc = fileNameList[len(fileNameList) - 3][:-2]
                if int(self.album.year) == 0:
                    self.album.year = fileNameList[1]
                elif self.album.year != fileNameList[1] and lockErrors == False:
                    lockErrors = True
                    self.errorCounter += 1
                    self.errors.append(ErrorEnum.FILES_ALBUM_YEAR_NOT_EQUAL)
                    self.album.year = -1


    def _analyseTracks(self):
        for fileName in self.files:
            trackTester = self._testFile(fileName, self.preservedPath, self.album)
            if trackTester != None:
                self.tracks.append(trackTester)


    # Manages the MP3 files to test in the pipeline
    def _testFile(self, fileName, pathList, album):
        audioTagPath = ''
        for folder in pathList: # Build the file path by concatenating folder in the file path
            audioTagPath += '{}/'.format(folder)
        audioTagPath += fileName # Append the filename at the end of the newly created path
        if fileName[-3:] == 'mp3' or fileName[-3:] == 'MP3': # Send the file path to the mutagen ID3 to get its tags and create the associated Track object
            track = Track('MP3', pathList, fileName, audioTagPath)
        elif fileName[-4:] == 'flac' or fileName[-4:] == 'FLAC':
            track = Track('FLAC', pathList, fileName, audioTagPath)
        else:
            return None
        return TrackTester(track, album)


    def tracksErrorCounter(self):
        errorCounter = 0
        for trackTester in self.tracks:
            errorCounter += trackTester.errorCounter
        return errorCounter
