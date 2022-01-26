# Python imports
import os
import fnmatch
# Project imports
from src.models.album import Album
from src.models.track import Track
from src.scan.trackTester import TrackTester
from src.utils.errorEnum import ErrorEnum


# AlbumTester aim to test all tracks in a folder and group all their errors
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


    # Analyse first the global album errors (compute a total disc/track and global album year)
    def _analyseAlbumInternals(self):
        lockErrors = False
        # Determine album title from path (if not properly named, will raise an error later on)
        self.album.albumTitle = self.preservedPath[len(self.preservedPath) - 1][7:] # Remove 7 first char of path (year and ' - ' separator)
        # Check that album folder does contains files
        if len(self.album.filesIterable) == 0:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.EMPTY_ALBUM_FOLDER)
        # Check that album folder does contains files
        if len(self.album.filesIterable) == 1 and len(fnmatch.filter(os.listdir('\\'.join(self.preservedPath)),'*.jpg')) == 1:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.ALBUM_ONLY_HAS_COVER)
        # Filling internals
        for fileName in self.album.filesIterable:
            if fileName[-3:] == 'MP3' or fileName[-3:] == 'mp3' or fileName[-4:] == 'FLAC' or fileName[-4:] == 'flac':
                self.album.totalTrack += 1
                forbiddenPattern = ['Single', 'Intro', 'ÉPILOGUE', '25', 'Interlude']
                fileNameList = fileName.split(' - ')
                # Re-join Single properly into list
                if len(fileNameList) == 7 and fileNameList[3] in forbiddenPattern:
                    # When album is a single, we must re-join the album name and the 'Single' suffix
                    fileNameList[2:4] = [' - '.join(fileNameList[2:4])]  # Re-join with a ' - ' separator
                # Fill internals
                if len(fileNameList) == 6 and int(fileNameList[len(fileNameList) - 3][:-2]) > int(self.album.totalDisc):
                    self.album.totalDisc = fileNameList[len(fileNameList) - 3][:-2]
                if len(fileNameList) == 6 and self.album.year == 0:
                    self.album.year = fileNameList[1]
        # Tracking errors
        for fileName in self.album.filesIterable:
            if fileName[-3:] == 'MP3' or fileName[-3:] == 'mp3' or fileName[-4:] == 'FLAC' or fileName[-4:] == 'flac':
                fileNameList = fileName.split(' - ')
                # ErrorCode 17 : Year is not the same on all physical files of the album
                if self.album.year != fileNameList[1] and lockErrors is False:
                    lockErrors = True
                    self.errorCounter += 1
                    self.errors.append(ErrorEnum.FILES_ALBUM_YEAR_NOT_EQUAL)
                    self.album.year = -1
        if len(fnmatch.filter(os.listdir('\\'.join(self.preservedPath)),'*.jpg')) != 1:
            self.errorCounter += 1
            self.errors.append(ErrorEnum.COVER_NOT_UNIQUE)


    # Analyse the album tracks (by creating a TrackTester for each)
    def _analyseTracks(self):
        for fileName in self.files:
            trackTester = self._testFile(fileName, self.preservedPath, self.album)
            if trackTester is not None:
                self.tracks.append(trackTester)


    @staticmethod
    # Manages the MP3/FLAC files to test in the pipeline
    def _testFile(fileName, pathList, album):
        audioTagPath = ''
        for folder in pathList:  # Build the file path by concatenating folder in the file path
            audioTagPath += '{}/'.format(folder)
        audioTagPath += fileName  # Append the filename at the end of the newly created path
        # Send the file path to the mutagen ID3 to get its tags and create the associated Track object
        if fileName[-3:] == 'mp3' or fileName[-3:] == 'MP3':
            track = Track('MP3', pathList, fileName, audioTagPath)
        elif fileName[-4:] == 'flac' or fileName[-4:] == 'FLAC':
            track = Track('FLAC', pathList, fileName, audioTagPath)
        else:
            return None
        return TrackTester(track, album)


    # Compute error counter for the album
    def tracksErrorCounter(self):
        if len(self.tracks) > 0:
            errorCounter = 0
            labelLockErrors = False
            languageLockErrors = False
            dateLockErrors = False
            albumLabel = self.tracks[0].track.label
            albumLanguage = self.tracks[0].track.lang
            albumDate = self.tracks[0].track.date
            for trackTester in self.tracks:
                errorCounter += trackTester.errorCounter
                # ErrorCode 30 : Label tag is not consistent over album tracks
                if trackTester.track.label != albumLabel and labelLockErrors is False:
                    labelLockErrors = True
                    self.errorCounter += 1
                    self.errors.append(ErrorEnum.INCONSISTENT_LABELS)
                # ErrorCode 31 : Language tag is not consistent over album tracks
                if trackTester.track.lang != albumLanguage and languageLockErrors is False:
                    languageLockErrors = True
                    self.errorCounter += 1
                    self.errors.append(ErrorEnum.INCONSISTENT_LANGUAGES)
                # ErrorCode 38 : Release date is not consistent accross album
                if trackTester.track.date != albumDate and dateLockErrors is False:
                    dateLockErrors = True
                    self.errorCounter += 1
                    self.errors.append(ErrorEnum.INCONSISTENT_RELEASE_DATE)
            return errorCounter
        return 0
