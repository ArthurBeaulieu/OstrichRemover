# Project imports
from src.models.album import Album
from src.models.track import Track

class AlbumCleaner:
    def __init__(self, files, preservedPath):
        self.preservedPath = preservedPath
        self.files = files
        self.album = Album(files)
        self._analyseAlbumInternals()
        self._analyseTracks()


    # Analyse first the global album errors (compute a total disc/track and global album year)
    def _analyseAlbumInternals(self):
        self.album.folderNameList = self.preservedPath[len(self.preservedPath) - 1].split(' - ');
        self.album.albumArtist = self.preservedPath[len(self.preservedPath) - 2]
        lockErrors = False
        # Filling internals
        for fileName in self.album.filesIterable:
            if fileName[-3:] == 'MP3' or fileName[-3:] == 'mp3' or fileName[-4:] == 'FLAC' or fileName[-4:] == 'flac':
                self.album.totalTrack += 1
            if fileName[-3:] == 'JPG' or fileName[-3:] == 'jpg' or fileName[-3:] == 'PNG' or fileName[-3:] == 'png':
              self.album.hasCover = True
              self.album.coverName = fileName


    # Analyse the album tracks
    def _analyseTracks(self):
        for fileName in self.files:
            self._cleanFile(fileName, self.preservedPath, self.album)


    # Manages the MP3/FLAC files to test in the pipeline
    def _cleanFile(self, fileName, pathList, album):
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
        track.clearInternalTags(self.album)
