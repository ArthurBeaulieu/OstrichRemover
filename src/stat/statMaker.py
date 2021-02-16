# Project imports
from src.models.album import Album
from src.models.track import Track


class StatMaker:
    def __init__(self, files, preservedPath):
        self.preservedPath = preservedPath
        self.files = files
        self.album = Album(files)
        self.tracks = []
        self.artists = []
        self.genres = []
        self.labels = []
        self.artistsDetails = []
        self._createTracks()
        self._analyzeTracks()


    def _createTracks(self):
        for fileName in self.files:
            track = self._createIndividualTrack(fileName, self.preservedPath, self.album)
            if track is not None:
                self.tracks.append(track)


    def _createIndividualTrack(self, fileName, pathList, album):
        audioTagPath = ''
        for folder in pathList:  # Build the file path by concatenating folder in the file path
            audioTagPath += '{}/'.format(folder)
        audioTagPath += fileName  # Append the filename at the end of the newly created path
        # Send the file path to the mutagen ID3 to get its tags and create the associated Track object
        if fileName[-3:] == 'mp3' or fileName[-3:] == 'MP3':
            return Track('MP3', pathList, fileName, audioTagPath)
        elif fileName[-4:] == 'flac' or fileName[-4:] == 'FLAC':
            return Track('FLAC', pathList, fileName, audioTagPath)
        else:
            return None


    def _analyzeTracks(self):
        for track in self.tracks:
            # Analyzing artists
            for artist in track.artists:
                if artist not in self.artists:
                    self.artistsDetails.append({
                        'artist': artist,
                        'info': [{
                            'album': track.albumTitle,
                            'albumArtist': track.albumArtist,
                            'as': 'artist'
                        }]
                    })
                    self.artists.append(artist)
            for performer in track.performers:
                if performer not in self.artists:
                    self.artistsDetails.append({
                        'artist': performer,
                        'info': [{
                            'album': track.albumTitle,
                            'albumArtist': track.albumArtist,
                            'as': 'performer'
                        }]
                    })
                    self.artists.append(performer)
            for composer in track.composers:
                if composer not in self.artists:
                    self.artistsDetails.append({
                        'artist': composer,
                        'info': [{
                            'album': track.albumTitle,
                            'albumArtist': track.albumArtist,
                            'as': 'composer'
                        }]
                    })
                    self.artists.append(composer)
            for producer in track.producers:
                if producer not in self.artists:
                    self.artistsDetails.append({
                        'artist': producer,
                        'info': [{
                            'album': track.albumTitle,
                            'albumArtist': track.albumArtist,
                            'as': 'producer'
                        }]
                    })
                    self.artists.append(producer)
            # Analyzing genres
            for genre in track.genres:
                if genre not in self.genres:
                    self.genres.append(genre)
            # Analyzing label
            if track.label not in self.labels:
                self.labels.append(track.label)
