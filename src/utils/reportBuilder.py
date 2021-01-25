# Python imports
import datetime
import json
import icu
# Project imports
from src.utils.errorEnum import ErrorEnum
from src.utils.tools import createDirectory


# Generate an JSON file from the albumTesters array
def computeFillReport(version, duration, folderInfo, albumTesters, errorCounter, purity):
    # Creating output dict object
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'folderInfo': _computeFolderInfo(folderInfo, errorCounter, purity),
        'artists': []
    }
    currentArtistName = ''
    currentArtist = {}
    for albumTester in albumTesters:
        albumPathList = albumTester.preservedPath
        if currentArtistName != albumPathList[len(albumPathList) - 2]:  # Current Artist has changed
            if currentArtist != {}:  # Avoid to add the first empty artist when loop starts
                output['artists'].append(currentArtist)
                currentArtist = {}
            currentArtistName = albumPathList[len(albumPathList) - 2]
            currentArtist['name'] = currentArtistName
            currentArtist['albums'] = []
        album = {
            'title': albumPathList[len(albumPathList) - 1],
            'errors': [],
            'tracks': []
        }
        for error in albumTester.errors:
            album['errors'].append(error.value)
        for trackTester in albumTester.tracks:
            if trackTester.errorCounter > 0:
                track = {
                    'title': trackTester.track.fileName,
                    'errors': []
                }
                for error in trackTester.errors:
                    track['errors'].append(error.value)
                album['tracks'].append(track)
        currentArtist['albums'].append(album)
    output['artists'].append(currentArtist)
    return output


# Generate an JSON file from the metaAnalyzer class
def computeMetaAnalyzeReport(version, duration, metaAnalyzer):
    # Creating output dict object
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'metaAnalyze': metaAnalyzer.metaAnalysis,
        'dumps': metaAnalyzer.dumps
    }
    return output


# Generate an JSON file from the metaAnalyzer class
def computeStatReport(version, duration, artists, genres, labels):
    # Creating output dict object
    collator = icu.Collator.createInstance(icu.Locale('fr_FR.UTF-8'))
    now = datetime.datetime.now()
    output = {
        'date': "{}-{}-{}".format(now.year, now.month, now.day),
        'version': version,
        'elapsedSeconds': duration,
        'count': {
            'artists': len(artists),
            'genres': len(genres),
            'labels': len(labels)
        },
        'artists': sorted(artists, key=collator.getSortKey),
        'genres': sorted(genres, key=collator.getSortKey),
        'labels': sorted(labels, key=collator.getSortKey)
    }
    return output



# Convert the folderInfo object into a returned dict
def _computeFolderInfo(folderInfo, errorCounter, purity):
    output = {
        'name': folderInfo.folder,
        'files': folderInfo.filesCounter,
        'folders': folderInfo.foldersCounter,
        'size': folderInfo.folderSize,
        'flacCount': folderInfo.flacCounter,
        'mp3Count': folderInfo.mp3Counter,
        'flacPercentage': folderInfo.flacPercentage,
        'mp3Percentage': folderInfo.mp3Percentage,
        'jpgPercentage': folderInfo.jpgPercentage,
        'pngPercentage': folderInfo.pngPercentage,
        'jpgCount': folderInfo.jpgCounter,
        'pngCount': folderInfo.pngCounter,
        'artistsCount': folderInfo.artistsCounter,
        'albumsCount': folderInfo.albumsCounter,
        'tracksCount': folderInfo.tracksCounter,
        'coversCount': folderInfo.coversCounter,
        'errorsCount': errorCounter,
        'possibleErrors': folderInfo.tracksCounter * len(ErrorEnum),
        'purity': purity
    }
    return output


# Save the output json file
def saveReportFile(report, directory):
    createDirectory(directory)
    fileName = "OstrichRemover-{}".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    with open('{}/{}.json'.format(directory, fileName), 'w') as file:
        json.dump(report, file, indent=2)
